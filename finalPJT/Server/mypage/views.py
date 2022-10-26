from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import  JsonResponse
import pandas as pd
import numpy as np
from lodgings.models import Like
from datetime import datetime
from lodgings.views import lodging_xlsx

tag_dic = {
    0 : "natural", 
    1 : "modern", 
    2 : "industrial", 
    3 : "classic", 
    4 : "popart",
    5 : "provence", 
    6 : "asia", 
}
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
    return dict_top4

def like_rader(like_list):
    df_lodging = lodging_xlsx()
    list_lod = list(like_list['lodging_id'].unique())
    list_lodging = df_lodging.loc[list_lod, ['lodging_name', 'address']]
    # df_lodging = pd.DataFrame(list_lodging, columns=['name', 'address'])
    temp = list_lodging.groupby(by='address').count().reindex()['lodging_name']
    result = dict(zip(temp.index, temp))
    return result

def like_pie(like_list):
    temp = like_list.groupby(by='lodging_id').count().reindex()['id']
    list_lodging = lodging_xlsx()
    val = list_lodging.iloc[temp.index]['tag'].value_counts().values
    val = val.tolist()

    index = list_lodging.iloc[temp.index]['tag'].value_counts().index
    result = dict(zip(index, val))
    return result

@api_view(['GET'])
@permission_classes([AllowAny])
def like_chart(request, user_id):
    result = {}
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))
    result['line'] = like_line(user_like)
    result['pie'] = like_pie(user_like)
    result['rader'] = like_rader(user_like)
    return JsonResponse({'graph': result}, json_dumps_params={'ensure_ascii': False}, status=200)

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




