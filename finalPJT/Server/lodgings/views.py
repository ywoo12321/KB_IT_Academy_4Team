from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Lodging
from .seriralizer import LodgingSerializer, SimpleLodgingSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def person_recom(request, user_id):

    pass

@api_view(['GET'])
@permission_classes([AllowAny])
def basic_recom(request):
    lodgings = get_list_or_404(Lodging)
    # 10개씩 쪼개기
    simpleserializer = SimpleLodgingSerializer(lodgings, many=True)
    simpleserializerdata =simpleserializer.data
    return JsonResponse({'data': simpleserializerdata[:10]}, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def lodging_detail(request, lodging_id):
    lodging = get_object_or_404(Lodging, pk=lodging_id)
    serializer = LodgingSerializer(lodging)
    # json으로 응답시 한글 깨짐 발생으로 인하여 ensure_ascii 사용
    return JsonResponse({'data': serializer.data}, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def sub_lodging(request, lodging_id):
    pass

@api_view(['GET'])
@permission_classes([AllowAny])
def search_lodging(request, keyward):
    answer = []
    # 숙소 이름과 관련있을 때
    contain_name = Lodging.objects.filter(lodging_name__icontains=keyward)
    # 숙소 지역으로 검색시
    contain_add = Lodging.objects.filter(lodging_address__icontains=keyward)
    # 분위기로 검색시
    if keyward=='모던' or (keyward.isapha()==True and keyward.lower=='mordern'):
        contain_tag = Lodging.objects.filter(tag=0)
        return Response(contain_tag)
    elif keyward=='네츄럴' or (keyward.isapha()==True and keyward.lower=='natural'):
        contain_tag = Lodging.objects.filter(tag=1)
    elif keyward=='클래식' or (keyward.isapha()==True and keyward.lower=='classic'):
        contain_tag = Lodging.objects.filter(tag=2)
    elif keyward=='인더스트리얼' or (keyward.isapha()==True and keyward.lower=='industrial'):
        contain_tag = Lodging.objects.filter(tag=3)
    elif keyward=='아시아' or (keyward.isapha()==True and keyward.lower=='aisa'):
        contain_tag = Lodging.objects.filter(tag=4)
    elif keyward=='프로방스' or (keyward.isapha()==True and keyward.lower=='provence'):
        contain_tag = Lodging.objects.filter(tag=5)
    elif keyward=='팝아트' or (keyward.isapha()==True and keyward.lower=='popart'):
        contain_tag = Lodging.objects.filter(tag=6)
    