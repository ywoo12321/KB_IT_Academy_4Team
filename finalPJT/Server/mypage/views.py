from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
from django.http import  JsonResponse
import pandas as pd
import numpy as np
from lodgings.models import Like
from datetime import datetime
from lodgings.views import lodging_xlsx, type_theme
import base64

import pickle, cv2
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Dense
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.train import latest_checkpoint

tag_dic = {i:v for i,v in enumerate(type_theme)}
total_local = "강원 경기 경상 광주 부산 서울 울산 인천 전라 제주 충청".split()
def like_line(like_list):
    df = like_list.copy()

    dt_now = datetime.now().year * 12 + datetime.now().month
    df['total_time'] = df['like_date'].astype('datetime64').dt.year * 12 + df['like_date'].astype('datetime64').dt.month
    temp = df[(df['total_time'] < dt_now) & (df['total_time'] > dt_now-4)]
    top4 = np.sort(temp['total_time'].unique())[:4]
    dict_top4 = {}
    df_lodging = lodging_xlsx()
    for i in top4:
        y = str(i // 12 if i % 12 != 0 else i // 12 - 1)
        m_temp = str(12 if i % 12 == 0 else i % 12)
        m = m_temp if len(m_temp) > 1 else '0'+m_temp
        
        temp_index = df[df['total_time']==i]['lodging_id'].value_counts().index
        lodging_object = df_lodging.loc[:,[*(tag_dic.values()), 'tag']]
        lodging_object = lodging_object.iloc[temp_index, :]

        dict_top4[y+"-"+m] = \
           [int((lodging_object[lodging_object['tag']==tag_dic[i]]).count()[i]) for i in range(7)]
        result = {}
    for i in type_theme:
        result[i] = []
    for key, value in dict_top4.items():
        for i, v in enumerate(value):
            result[tag_dic[i]].append(v)
    return result

def like_pie(like_list):
    df_lodging = lodging_xlsx()
    list_lod = list(like_list['lodging_id'].unique())
    list_lodging = df_lodging.loc[list_lod, ['lodging_name', 'address']]

    temp = list_lodging.groupby(by='address').count().reindex()['lodging_name']
    result = dict(zip(temp.index, temp))
    for i in total_local:
        if result.get(i) == None:
            result[i] = 0
    return result

def like_rader(like_list):
    temp = like_list.groupby(by='lodging_id').count().reindex()['id']
    list_lodging = lodging_xlsx()
    val = list_lodging.iloc[temp.index]['tag'].value_counts().values
    val = val.tolist()

    index = list_lodging.iloc[temp.index]['tag'].value_counts().index
    result = dict(zip(index, val))
    for i in type_theme:
        if result.get(i) == None:
            result[i] = 0
    return result

@api_view(['GET'])
@permission_classes([AllowAny])
def like_chart(request, user_id):
    result = {}
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))
    result['line'] = like_line(user_like)
    result['pie'] = like_pie(user_like)
    result['rader'] = like_rader(user_like)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def like_list(request, user_id):
    lodging_list = lodging_xlsx()
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))['lodging_id']
    like_list = list(Like.objects.filter(user_id=user_id).values_list('lodging_id'))
    
    result = {}
    for i in like_list:
        temp = {}
        temp['name'] = lodging_list.loc[i[0], 'lodging_name']
        temp['img'] = lodging_list.loc[i[0], 'img1']
        result[i[0]] = temp
    return JsonResponse({'like': result}, json_dumps_params={'ensure_ascii': False}, status=200)

'''--------------------------------------------------------------------------------------------'''

def prepare_image(image, target_width=224, target_height=224, max_zoom=0.2):
    height = image.shape[0]
    width = image.shape[0]

    image_ratio = width / height
    target_image_ratio = target_width / target_height
    
    crop_vertically = image_ratio < target_image_ratio
    crop_width = width if crop_vertically else int(height * target_image_ratio)
    crop_height = int(width / target_image_ratio) if crop_vertically else height

    resize_factor = np.random.rand() * max_zoom + 1.0
    crop_width = int(crop_width / resize_factor)
    crop_height = int(crop_height / resize_factor)

    x0 = np.random.randint(0, width - crop_width)
    y0 = np.random.randint(0, height - crop_height)
    x1 = x0 + crop_width
    y1 = y0 + crop_height

    image = image[y0:y1, x0:x1]

    if np.random.rand() < 0.5:
        image = np.fliplr(image)

    try:
      image = cv2.resize(image, (target_width, target_height))
    except:
      print("error")
      pass
    return image.astype(np.float32) / 255

def make_prediction(model, img_path):
    # model = load_model()
    origin = [os.getcwd(), 'theme', 'dataset2_pkl.pkl']
    with open(os.path.join(*origin), 'rb') as f:
        class_dict = pickle.load(f)
    # print(class_dict)
    img_tmp = cv2.imread(img_path, 1)
    image = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    image = prepare_image(image)
    images = []
    images.append(image)
    images = np.array(images)
    image_size = 224
    n_channels = 3
    X_batch = images.reshape(1, image_size, image_size, n_channels)

    preds = model.predict(X_batch)

    top_7 = np.argpartition(preds[0], -1)[-1:]
    top_7 = reversed(top_7[np.argsort(preds[0][top_7])])
    
    result = ''
    for i in top_7:
        result = '{0}: {1:.2f}%'.format(class_dict[i], 100 * preds[0][i])
    return result
@api_view(['POST'])
@permission_classes([AllowAny])
def image_class(request):
    agumon = os.path.join(os.getcwd(), 'theme', 'test.jpg')
    try:
        os.remove(agumon)
        file = request.data['image']
        fs = FileSystemStorage()

    except:
        file = request.data['image']
        fs = FileSystemStorage()
    fs.save(agumon, file)
    # origin = [os.getcwd(), 'theme', 'checkpoints']
    IMG_SIZE = 224
    conv_base = MobileNet(weights='imagenet',
                    include_top=False,
                    input_shape=(IMG_SIZE, IMG_SIZE, 3))
    conv_base.trainable = True
    model = Sequential([
        conv_base,
        GlobalAveragePooling2D(),
        Dropout(0.5),
        Dense(1000, activation='relu'),
        Dense(500, activation='relu'),
        Dense(7, activation='softmax'),
    ])
    # latest = latest_checkpoint(os.path.join(*origin))
    # model.load_weights(latest)
    result = make_prediction(model, agumon)
    return JsonResponse({'like': result}, json_dumps_params={'ensure_ascii': False}, status=200)