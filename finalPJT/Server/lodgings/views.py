from django.http import  JsonResponse, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Count
from .models import Like
from accounts.models import Prefer
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import os

def norm_cal(a,b):
    return round(dot(a,b)/(norm(a)*norm(b)), 3)

def lodging_xlsx():
    path = os.path.join(os.getcwd(), 'theme', 'type.xlsx')
    df = pd.read_excel(path)
    return df

def cal(prefer):
    df = lodging_xlsx()
    df['cosine'] = df[['내츄럴', '모던' ,'인더스트리얼', '클래식', '팝아트', '프로방스', '한옥']].apply(lambda x:norm_cal(prefer, x), axis=1)
    df = df.sort_values(by='cosine', ascending=False)
    return df.head(20)

# basic + personal recommend
@api_view(['GET'])
@permission_classes([AllowAny])
def person_recom(request, user_id):
    # user_filtering = Prefer.objects.filter(user_id=user_id).values()
    temp = Prefer.objects.get(user_id=user_id)
    user_filtering = temp.values()      
    user_prefer = user_filtering[0] if len(user_filtering) > 0 else [0,0,0,0,0,0,0]
    input = [user_prefer[i] for i in user_prefer.keys()][1:]

    like_filtering = Like.objects.filter(user_id=user_id).values()
    tag_dic = {
        "modern": 0,
        "natural": 1,
        "classic": 2,
        "industry": 3,
        "asia": 4,
        "provence": 5,
        "unique": 6
    }

    '''
    가중치 초기화
    w = [ 0 for i in range(7)]

    찜을 한 것중에서 숙소를 찾고 그 숙소의 가중치를 w에 더하기
    for i in like_filtering:
        id = i['lodging_id_id']
        lod = Lodging.objects.get(id = id).values()
        temp = [lod[i] for i in tag_dic]
        w = [x+y for x,y in zip(w, temp)]

    input = [x+y for x,y in zip(input, w)]
    '''

    # cols = list(map(lambda x : str(x).split('.')[-1], user_prefer._meta.fields))
    # inputs = [ user_prefer[i] for i in cols ]
    # print(user_prefer.)
    answer = cal(input)
    return JsonResponse({'search':answer.to_dict()}, json_dumps_params={'ensure_ascii': False}, status=200)



# basic = top10 + tag interior(random)
@api_view(['GET'])
@permission_classes([AllowAny])
def basic_recom(request):
    lodg = lodging_xlsx()

    basic_recommendation = {}
    # 인기있는 숙소 top10
    hot_list = (Like.objects.values('lodging_id').annotate(dcount=Count('lodging_id'))).order_by('-dcount')[:10]
    hot_lodging = []
    print(hot_lodging)
    # # range(10)으로 할 경우 위에서 10개까지 slice 안 될 경우 error발생으로 len(hot_list)으로 작성
    # for h in range(len(hot_list)):
    #     lodging_pk = hot_list[h]['lodging_id']

    #     # hot_lodging.append(simple_serializer.data)
    # basic_recommendation['hot'] = hot_lodging
    
    # interior tag별 data 20개씩 추가
    # !--- random 추가해야합니다 ---! 
    interior = ["Modern", "Natural", "Classic", "Industrial", "Asia", "Provence", "Pop Art"]
    # for t in range(7):
        # tag_list = Lodging.objects.filter(tag=t)[:20]
        # simple_serializer = SimpleLodgingSerializer(tag_list, many=True)
        # basic_recommendation[interior[t]] = list(simple_serializer.data)
    return JsonResponse(basic_recommendation, json_dumps_params={'ensure_ascii': False}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def lodging_detail(request, lodging_id):
    lodging = get_object_or_404(Lodging, pk=lodging_id)
    serializer = LodgingSerializer(lodging)
    # json으로 응답시 한글 깨짐 발생으로 인하여 ensure_ascii 사용
    return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=200)


# !--- random 추가해야합니다 ---! 
@api_view(['GET'])
@permission_classes([AllowAny])
def sub_lodging(request, lodging_id):
    sub_lodgings = {}
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
    return JsonResponse(sub_lodgings, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_lodging(request, keyward):
    tag_dic = {
        "modern": 0,
        "natural": 1,
        "classic": 2,
        "industry": 3,
        "asia": 4,
        "provence": 5,
        "unique": 6
    }
    result1 = Lodging.objects.filter(lodging_name__contains=keyward)
    result2 = Lodging.objects.filter(lodging_address__contains=keyward)
    result = result1.union(result2)
    if keyward in tag_dic:
        result3 = Lodging.objects.filter(tag=tag_dic[keyward])
        result = result.union(result3)
    answer = SimpleLodgingSerializer(result, many=True).data
    return JsonResponse({'search':answer}, json_dumps_params={'ensure_ascii': False}, status=200)

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
