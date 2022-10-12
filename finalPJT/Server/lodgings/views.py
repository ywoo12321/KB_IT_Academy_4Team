from django.http import  JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db.models import Count
from .models import Lodging, Like
from .serializer import LodgingSerializer, SimpleLodgingSerializer
from accounts.models import Prefer


# basic + personal recommend
@api_view(['GET'])
@permission_classes([AllowAny])
def person_recom(request, user_id):
    person_recommendation = {}
    # index별 유저의 선호도 수치 조사
    if Prefer.objects.filter(user_id=user_id).exists():
        user = get_object_or_404(Prefer, user_id=user_id)
        user_tag_prefer = []
        user_tag_prefer.append(user.prefer_modern)
        user_tag_prefer.append(user.prefer_natural)
        user_tag_prefer.append(user.prefer_classic)
        user_tag_prefer.append(user.prefer_industry)
        user_tag_prefer.append(user.prefer_asia)
        user_tag_prefer.append(user.prefer_provence)
        user_tag_prefer.append(user.prefer_unique)
        # max값이 존재할 때, (두가지 일 경우) > 비율로 추천해 주는 것이 좋지 않을까?
        
        # 최댓값 tag index 확인
        most_prefer = user_tag_prefer.index(max(user_tag_prefer))
        person_recom['favor'] = LodgingSerializer

    # 만일, user의 prefer가 존재하지 않을 경우 (미실시)
    else:
        pass
    # basic recommendation 추가
    return JsonResponse(person_recommendation, json_dumps_params={'ensure_ascii': False}, status=200)


# basic = top10 + tag interior(random)
@api_view(['GET'])
@permission_classes([AllowAny])
def basic_recom(request):
    basic_recommendation = {}
    # 인기있는 숙소 top10
    hot_list = (Like.objects.values('lodging_id').annotate(dcount=Count('lodging_id'))).order_by('-dcount')[:10]
    hot_lodging = []
    # range(10)으로 할 경우 위에서 10개까지 slice 안 될 경우 error발생으로 len(hot_list)으로 작성
    for h in range(len(hot_list)):
        lodging_pk = hot_list[h]['lodging_id']
        lodging = get_object_or_404(Lodging, pk=lodging_pk)
        simple_serializer = SimpleLodgingSerializer(lodging)
        hot_lodging.append(simple_serializer.data)
    basic_recommendation['hot'] = hot_lodging
    
    # interior tag별 data 20개씩 추가
    # !--- random 추가해야합니다 ---! 
    interior = ["Modern", "Natural", "Classic", "Industrial", "Asia", "Provence", "Pop Art"]
    for t in range(7):
        tag_list = Lodging.objects.filter(tag=t)[:20]
        simple_serializer = SimpleLodgingSerializer(tag_list, many=True)
        basic_recommendation[interior[t]] = list(simple_serializer.data)
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
