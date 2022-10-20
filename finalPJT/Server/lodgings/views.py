from django.http import  JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Count
from .models import Like
from accounts.models import Prefer
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import os, random

type_theme = ['modern', 'natural',  'classic', 'industrial', 'asia', 'provence', 'popart']

def norm_cal(a,b):
    return round(dot(a,b)/(norm(a)*norm(b)), 3)

def lodging_xlsx():
    path = os.path.join(os.getcwd(), 'theme', 'type.xlsx')
    df = pd.read_excel(path)
    return df

def cal(prefer):
    df = lodging_xlsx()
    df['cosine'] = df[type_theme].apply(lambda x:norm_cal(prefer, x), axis=1)
    df = df.sort_values(by='cosine', ascending=False)
    return df.head(21)

# basic + personal recommend
@api_view(['GET'])
@permission_classes([AllowAny])
def person_recom(request, user_id):
    theme = \
    ['prefer_modern',
    'prefer_natural',
    'prefer_classic',
    'prefer_industry',
    'prefer_asia',
    'prefer_provence',
    'prefer_unique',]

    temp = Prefer.objects.get(user_id_id=user_id).__dict__
    del temp['_state']
    
    user_prefer = [temp[i] for i in theme]
    list_lodging = lodging_xlsx()
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))
    index_lod = list(user_like['lodging_id'].unique())
    temp2 = list_lodging.iloc[index_lod, :].sum()[type_theme].values
    user_prefer = [ x + y for x,y in zip(user_prefer, temp2)]
    answer = cal(user_prefer).drop('Unnamed: 0', axis=1).reset_index().rename(columns={'index':'lodging_id', 'img1':'lodging_img' })[['lodging_id', 'lodging_name','tag','address', 'lodging_img']]
    return JsonResponse(answer.to_dict(orient='records'),safe=False, json_dumps_params={'ensure_ascii': False},  status=200)



# basic = top10 + tag interior(random)
@api_view(['GET'])
@permission_classes([AllowAny])
def basic_recom(request):
    lodging_file = lodging_xlsx()

    basic_recommendation = {}
    # 인기있는 숙소 top10
    hot_list = (Like.objects.values('lodging_id').annotate(dcount=Count('lodging_id'))).order_by('-dcount')[:10]
    hot_lodging = []

    # range(10)으로 할 경우 위에서 10개까지 slice 안 될 경우 error발생으로 len(hot_list)으로 작성
    for h in range(len(hot_list)):
        lodging = {}
        lodging_idx = hot_list[h]['lodging_id']
        lodging['lodging_id'] = lodging_idx
        lodging['lodging_name'] = lodging_file.loc[lodging_idx]['lodging_name']
        lodging['lodging_img'] = lodging_file.loc[lodging_idx]['img1']
        hot_lodging.append(lodging)
    basic_recommendation['hot'] = hot_lodging
    
    # interior tag별 data 20개씩 추가
    # interior_list = ['natural', 'modern', 'industrial', 'classic', 'popart', 'provence', 'asia']
    for interior in type_theme:
        # tag 별 가장 성향이 높은 30개의 index
        theme_idx = list(lodging_file.sort_values(interior, ascending=False).head(30).index)
        # 30개 중 20개 random하게 추출
        random_lodg = random.sample(theme_idx, 20)
        temp = []
        for ran in random_lodg:
            lodging = {}
            lodging['lodging_id'] = ran
            lodging['lodging_name'] = lodging_file.loc[ran]['lodging_name']
            lodging['lodging_img'] = lodging_file.loc[ran]['img1']
            temp.append(lodging)
        basic_recommendation[interior] = temp
    return JsonResponse(basic_recommendation, json_dumps_params={'ensure_ascii': False}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def lodging_detail(request, lodging_id):
    lodging_file = lodging_xlsx()
    # 해당 index가 file에 존재할 경우
    if lodging_id in lodging_file.index:
        lodging_data = {}
        lod = lodging_file.loc[lodging_id]
        lodging_data["lodging_id"] = lodging_id
        lodging_data["lodging_name"] = lod.loc["lodging_name"]
        lodging_data["tag"] = lod.loc["tag"]
        lodging_data["address"] = lod.loc["address"]
        lodging_data["img1"] = lod.loc["img1"]
        lodging_data["img2"] = lod.loc["img2"]
        lodging_data["img3"] = lod.loc["img3"]
        return JsonResponse(lodging_data, json_dumps_params={'ensure_ascii': False}, status=200)

    # lodging_id가 file에 존재하지 않는 경우
    else:
        return JsonResponse(status=404, data={'status':'false','message':'해당하는 숙소는 존재하지 않습니다.'})



@api_view(['GET'])
@permission_classes([AllowAny])
def sub_lodging(request, lodging_id):
    lodging_file = lodging_xlsx()
    result = {
        'sametheme': [],
        'samelocation': [],
    }
    # 해당 index가 file에 존재할 경우
    if lodging_id in lodging_file.index:
        # 현재 lodging의 theme값들을 가져옴
        now_theme = list(lodging_file.loc[lodging_id][2:9])
        theme_idx = list(cal(now_theme).index)
        for idx in theme_idx[1:]:
            lodging = {}
            lodging['lodging_id'] = idx
            lodging['lodging_name'] = lodging_file.loc[idx]['lodging_name']
            lodging['lodging_img'] = lodging_file.loc[idx]['img1']
            result['sametheme'].append(lodging)
        # 현재 지역과 같은 지역에 있는 숙소를 random하게 추출
        now_location = lodging_file.loc[lodging_id]['address']
        location = list(lodging_file.loc[(lodging_file['address']==now_location) & (lodging_file[lodging_id] != idx)])
        print(location)
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False}, status=200)

    # lodging_id가 file에 존재하지 않는 경우
    else:
        return JsonResponse(status=404, data={'status':'false','message':'해당하는 숙소는 존재하지 않습니다.'})
    '''sub_lodgings = {}
    lodging = get_object_or_404(Lodging, pk=lodging_id)
    # 현재 숙소를 제외한 같은 tag 20개를 sametheme로 넣어줌
    lod_tag = Lodging.objects.exclude(pk=lodging_id).filter(tag=lodging.tag)[:20]
    lod_tag_serializers = SimpleLodgingSerializer(lod_tag, many=True)
    sub_lodgings['sametheme'] = lod_tag_serializers.data
    # 현재 숙소를 제외한 같은 주소 20개를 sametheme로 넣어줌
    # 주소 api 어떻게 받아오느냐에 따라 코드 변경
    lod_add = Lodging.objects.exclude(pk=lodging_id).filter(lodging_address=lodging.lodging_address)[:20]
    lod_add_serializers = SimpleLodgingSerializer(lod_add, many=True)
    sub_lodgings['samelocation'] = lod_add_serializers.data
    return JsonResponse(sub_lodgings, json_dumps_params={'ensure_ascii': False}, status=200)'''

@api_view(['GET'])
@permission_classes([AllowAny])
def search_lodging(request, keyword):
    tag_dic = {
        "modern": 0,
        "natural": 1,
        "classic": 2,
        "industry": 3,
        "asia": 4,
        "provence": 5,
        "unique": 6
    }
    input_list = sum(list(map(lambda x : x.split(), keyword.split(','))), [])
    finds = []
    check = '|'.join(input_list)
    df_lodging = lodging_xlsx()
    finds.extend(df_lodging[df_lodging['lodging_name'].str.contains(check)]['Unnamed: 0'].index.values)
    finds.extend(df_lodging[df_lodging['address'].str.contains(check)]['Unnamed: 0'].index.values)
    finds.extend(df_lodging[df_lodging['tag'].str.contains(check)]['Unnamed: 0'].index.values)
    find_index = sorted(list(set(finds)))
    answer = df_lodging.iloc[find_index].drop('Unnamed: 0', axis=1).reset_index().rename(columns={'index':'lodging_id', 'img1':'lodging_img' })[['lodging_id', 'lodging_name','tag','address', 'lodging_img']]
    return JsonResponse(answer.to_dict(orient='records'),safe=False, json_dumps_params={'ensure_ascii': False},  status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def image_response(request, lodging_id):
    result1 = Lodging.objects.filter(id=lodging_id)
    if len(result1) > 0:
        r = result1.values()[0]
        origin = [os.getcwd(),]
        origin.extend(r['lodging_img1'].split('/'))
        path = os.path.join(*origin)
        img = open(path, 'rb')
        return HttpResponse(img, content_type='image/jpeg')
    else:
        return JsonResponse({'img': "None"}, json_dumps_params={'ensure_ascii': False}, status=200)
