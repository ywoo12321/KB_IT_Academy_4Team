from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Lodging
from .serializer import LodgingSerializer, SimpleLodgingSerializer

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
    tag_dic = {
        "modern" :0,
        "natural" :1,
        "classic" :2,
        "industry" :3,
        "asia" :4,
        "provence" :5,
        "unique" :6
    }
    result1 = Lodging.objects.filter(lodging_name__contains=keyward)
    result2 = Lodging.objects.filter(lodging_address__contains=keyward)
    result = result1.union(result2)
    if keyward in tag_dic:
        result3 = Lodging.objects.filter(tag=tag_dic[keyward])
        result = result.union(result3)
    search = ",".join(map(lambda x: '\''+x.lodging_name+'\'', result))
    return JsonResponse({'search': "[" + search + "]"}, json_dumps_params={'ensure_ascii': False}, status=200)