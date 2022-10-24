from django.http import  JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Count

from .models import Like
from accounts.models import Prefer, Account
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import os, random

type_theme = ['modern', 'natural',  'classic', 'industrial', 'asia', 'provence', 'popart']

# 코사인 계산 함수
def norm_cal(a,b):
    return round(dot(a,b)/(norm(a)*norm(b)), 3)
# 파일 읽기
def lodging_xlsx():
    path = os.path.join(os.getcwd(), 'theme', 'type.xlsx')
    df = pd.read_excel(path).copy()
    return df
# 코사인 유사도 계산
def cal(prefer):
    df = lodging_xlsx()
    df['cosine'] = df[type_theme].apply(lambda x:norm_cal(prefer, x), axis=1)
    df = df.sort_values(by='cosine', ascending=False)
    return df.head(21)

# 인기있는 숙소 top10
def hot_maker(basic_recommendation):
    lodging_file = lodging_xlsx()
    hot_list = (Like.objects.values('lodging_id').annotate(dcount=Count('lodging_id'))).order_by('-dcount')[:10]
    hot_lodging = []
    # range(10)으로 할 경우 위에서 10개까지 slice 안 될 경우 error발생으로 len(hot_list)으로 작성
    for i in hot_list:
        lodging = {}
        lodging_idx = i['lodging_id']
        lodging['lodging_id'] = lodging_idx
        lodging['lodging_name'] = lodging_file.loc[lodging_idx]['lodging_name']
        lodging['lodging_img'] = lodging_file.loc[lodging_idx]['img1']
        hot_lodging.append(lodging)
    basic_recommendation[len(basic_recommendation.keys())] = hot_lodging
    return basic_recommendation

# 태그별 숙소
def tag_maker(basic_recommendation):
    lodging_file = lodging_xlsx()
    for index, interior in enumerate(type_theme):
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
        basic_recommendation[len(basic_recommendation.keys())] = temp
    return basic_recommendation

# 취향 저격 숙소
def snipe_maker(personal_recommend, user_id):
    theme = \
    ['prefer_modern',
    'prefer_natural',
    'prefer_classic',
    'prefer_industry',
    'prefer_asia',
    'prefer_provence',
    'prefer_unique',]
    list_lodging = lodging_xlsx()

    temp = Prefer.objects.get(user_id_id=user_id).__dict__
    del temp['_state']

    user_prefer = [temp[i] for i in theme]

    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))
    index_lod = list(user_like['lodging_id'].unique())
    temp2 = list_lodging.iloc[index_lod, :].sum()[type_theme].values

    user_prefer = [ x + y for x,y in zip(user_prefer, temp2)]
    answer = cal(user_prefer).drop('Unnamed: 0', axis=1).reset_index().rename(columns={'index':'lodging_id', 'img1':'lodging_img' })[['lodging_id', 'lodging_name','tag','address', 'lodging_img']]
    personal_recommend[len(personal_recommend.keys())] = answer.to_dict(orient='records')
    return personal_recommend
# 지역 기반 추천
'''
 1. 주소를 전처리하는 과정이 필요함 oR 전처리해서 들어오기
 2. temp['address'] 에서 str를 지정했지만 주소가 문자열이 되면 그럴 필요가 없음.
'''
def local_maker(personal_recommend, user_id):
    local_list = []
    list_lodging = lodging_xlsx()
    # 현재는 그냥 주소를 0~7 로 임의지정 해씀다
    user_address = Account.objects.filter(user_id = user_id).values_list('address')[0][0]
    user_address = 2
    near_user = list(list_lodging[list_lodging['address']==user_address].index)
    random.shuffle(near_user)
    for i in near_user:
        if len(local_list) > 20:
            break
        temp = {}
        temp['lodging_id'] = int(i)
        temp['lodging_name'] = list_lodging.loc[i]['lodging_name']
        temp['tag'] = list_lodging.loc[i]['tag']
        temp['address'] = str(list_lodging.loc[i]['address'])
        temp['lodging_img'] = list_lodging.loc[i]['img1']
        local_list.append(temp)
    personal_recommend[len(personal_recommend.keys())] = local_list
    return personal_recommend
# 회원
# basic + personal recommend
@api_view(['GET'])
@permission_classes([AllowAny])
def person_recom(request, user_id):
    personal_recommend = {}
    snipe_maker(personal_recommend, user_id)
    local_maker(personal_recommend, user_id)
    hot_maker(personal_recommend)
    tag_maker(personal_recommend)
    return JsonResponse([personal_recommend] ,safe=False, json_dumps_params={'ensure_ascii': False},  status=200)

# 비회원
# basic = top10 + tag interior(random)
@api_view(['GET'])
@permission_classes([AllowAny])
def basic_recom(request):
    basic_recommendation = {}
    hot_maker(basic_recommendation)
    # interior tag별 data 20개씩 추가
    # interior_list = ['natural', 'modern', 'industrial', 'classic', 'popart', 'provence', 'asia']
    tag_maker(basic_recommendation)
    # 개수 확인을 위한 test
    # for i in basic_recommendation.keys():
    #     print(len(basic_recommendation[i]))
    return JsonResponse([basic_recommendation], safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def lodging_detail(request, lodging_id):
    lodging_file = lodging_xlsx()
    result = {
        'lodging' : [],
        'sametheme': [],
        'samelocation': [],
    }
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
        result['lodging'].append(lodging_data)

        # 현재 lodging과 cos유사도가 가장 높은 숙소들을 가져옴
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
        condition = (lodging_file['address']==now_location)
        location_idx = list(lodging_file.loc[condition].drop(lodging_id).index)
        # 20개 random하게 추출
        lodg = random.sample(location_idx, 20)
        for lod in lodg:
            lodging = {}
            lodging['lodging_id'] = lod
            lodging['lodging_name'] = lodging_file.loc[lod]['lodging_name']
            lodging['lodging_img'] = lodging_file.loc[lod]['img1']
            result['samelocation'].append(lodging)
        return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

    # lodging_id가 file에 존재하지 않는 경우
    else:
        return JsonResponse(status=404, data={'status':'false','message':'해당하는 숙소는 존재하지 않습니다.'})

@api_view(['GET'])
@permission_classes([AllowAny])
def search_lodging(request, keyword):
    input_list = sum(list(map(lambda x : x.split(), keyword.split(','))), [])
    finds = []
    check = '|'.join(input_list)
    df_lodging = lodging_xlsx()
    finds.extend(df_lodging[df_lodging['lodging_name'].str.contains(check)]['Unnamed: 0'].index.values)
    finds.extend(df_lodging[df_lodging['address'].str.contains(check)]['Unnamed: 0'].index.values)
    finds.extend(df_lodging[df_lodging['tag'].str.contains(check)]['Unnamed: 0'].index.values)
    find_index = sorted(list(set(finds)))
    answer = df_lodging.iloc[find_index].drop('Unnamed: 0', axis=1).reset_index().rename(columns={'index':'lodging_id', 'img1':'lodging_img' })[['lodging_id', 'lodging_name','tag','address', 'lodging_img']]
    return JsonResponse([answer.to_dict(orient='records')],safe=False, json_dumps_params={'ensure_ascii': False},  status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def random_maker(request):
    result_dict = {}
    random_dict = {}
    url = request.build_absolute_uri().replace('random', 'image')
    origin = [os.getcwd(), 'theme', 'traindata']
    pop_list = ['provence', 'classic', 'popart']
    theme_list = (type_theme.copy())*3
    random.shuffle(theme_list)
    theme_list.remove(random.choice(pop_list))
    for i,v in enumerate(theme_list):
        if v not in random_dict:
            temp = origin + [v]
            random_dict[v] = os.listdir(os.path.join(*temp))
        temp_dict = {}
        temp_dict['src'] = url + v + '/'+ random_dict[v].pop(random.choice(range(len(random_dict[v]))))
        temp_dict['tag'] = type_theme.index(v)
        result_dict['image'+str(i+1)] = temp_dict
    return JsonResponse([result_dict], json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def image_response(request, theme, keyword):
    try:
        origin = [os.getcwd(), 'theme', 'traindata', theme, keyword]
        path = os.path.join(*origin)
        img = open(path, 'rb')
        return HttpResponse(img, content_type='image/jpeg')
    except:
        return JsonResponse({'img': "None"}, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def like(request, user_id, lodging_id):
    try : 
        lodging_list = lodging_xlsx()
        search = lodging_list[lodging_list['Unnamed: 0']==int(lodging_id)]
        if len(search) == 0:
            raise Exception('존재하지 않는 숙소입니다.')
        user = Account.objects.filter(user_id=user_id)
        if not user.exists():
            raise Exception('존재하지 않는 유저입니다.')
        likes = Like.objects.filter(user_id=user_id)
        tt = set(map(lambda x : x[0], list(likes.values_list('lodging_id'))))
        if lodging_id not in tt:
            user_data = user.values('user_id')[0]
            l = Like()
            l.user_id_id = user_data["user_id"]
            l.lodging_id = lodging_id
            l.save()
        else:
            raise Exception('이미 찜을 하였습니다.')
        return JsonResponse({'result': "True", 'message': '성공'}, json_dumps_params={'ensure_ascii': False}, status=200)
    except Exception as e:
        return JsonResponse({'result': "False", 'message': str(e)}, json_dumps_params={'ensure_ascii': False}, status=200)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def dislike(request, user_id, lodging_id):
    try : 
        lodging_list = lodging_xlsx()
        search = lodging_list[lodging_list['Unnamed: 0']==int(lodging_id)]
        if len(search) == 0:
            raise Exception('존재하지 않는 숙소입니다.')
        user = Account.objects.filter(user_id=user_id)
        if not user.exists():
            raise Exception('존재하지 않는 유저입니다.')
        likes = Like.objects.filter(user_id=user_id)
        tt = set(map(lambda x : x[0], list(likes.values_list('lodging_id'))))
        if lodging_id not in tt:
            raise Exception('찜한 기록이 없습니다.')
        my_like = likes.filter(lodging_id = lodging_id)
        my_like.delete()
        return JsonResponse({'result': "True", 'message': '성공'}, json_dumps_params={'ensure_ascii': False}, status=200)
    except Exception as e:
        return JsonResponse({'result': "False", 'message': str(e)}, json_dumps_params={'ensure_ascii': False}, status=200)