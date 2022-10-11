from gc import get_objects
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import AccountSerializer, PreferSerializer
from .models import Account, Prefer

@api_view(['GET'])
@permission_classes([AllowAny])
def check_id(request, user_id):
    try:
        return JsonResponse({"isUnique": not Account.objects.filter(user_id=user_id).exists()})
    except Account.DoesNotExist:
        # 존재하지 않는 경우에도 unique 이기 때문
        return JsonResponse({"isUnique": True})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def prefer_test(request, user_id):
    prefer = get_object_or_404(Prefer, user_id=user_id)
    modern = prefer.prefer_modern
    content = {
        'modern' : prefer.prefer_modern,
        'provence' : prefer.prefer_provence,
    }
    return JsonResponse(content)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method=='POST':
        try:
            user_id = request.data['userid']
            check = Account.objects.filter(user_id=user_id)
            if len(check) == 0:
                return JsonResponse({"code":200, "message":"Fail, 존재하지 않는 아이디"})
            elif check[0].password == request.data['password']:
                return JsonResponse({"code":200, "message":"Success 로그인 성공"})
            else:
                return JsonResponse({"code":200, "message":"Fail, 비밀번호 불일치"})    
        except Account.DoesNotExist:
            return JsonResponse({"code":200, "message":"Fail, 존재하지 않는 아이디"})
    else:
        return JsonResponse({"code":200, "message":"Fail, 잘못된 요청"})


@api_view(['POST'])
@permission_classes([AllowAny])
def join(request):
    pass
    # if request.method=='POST':
    #     user_id = request.data['userid']
    #     # prefer = 
    #     check = get_objects(Account, pk=user_id)
    #     if check is None:
    #         account_serializer = AccountSerializer(data=request.data)
    #         account_serializer.save()
    #         # prefer 정보를 어떻게 전달? 문자열로 전달?
    #         if request.data['']
    #         prefer_serializer = PreferSerializer(data=)
    #     else : 
    #         return JsonResponse({"code":200, "message":"Fail, 이미 존재한 아이디"})    
    # else:
    #     return JsonResponse({"code":200, "message":"Fail, 잘못된 요청"})