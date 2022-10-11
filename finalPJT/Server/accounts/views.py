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

import json

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
    if request.method=='POST':
        try:
            data = request.data
            data['user_id'] = data['userid']
            pf = {"user_id": data['user_id'],
            "prefer_modern" : int(data['prefer'][0]),
            "prefer_natural" : int(data['prefer'][1]),
            "prefer_classic" : int(data['prefer'][2]),
            "prefer_industry" : int(data['prefer'][3]),
            "prefer_asia" : int(data['prefer'][4]),
            "prefer_provence" : int(data['prefer'][5]),
            "prefer_unique" : int(data['prefer'][6]),
                }
            del data['userid']
            del data['prefer']
            acSerializer= AccountSerializer(data=data)
            if acSerializer.is_valid(raise_exception=True):
                acSerializer.save()
                pfSerializer = PreferSerializer(data=pf)
                if pfSerializer.is_valid(raise_exception=True):
                    pfSerializer.save()
            return JsonResponse({"code":200, "message":"Success 회원가입 성공"}, json_dumps_params={'ensure_ascii': False}, status=200)
        except Exception:
            return JsonResponse({"code":200, "message":"Fail 회원가입 실패"}, json_dumps_params={'ensure_ascii': False}, status=200)
    else:
        return JsonResponse({"code":200, "message":"잘못된 요청"}, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_user_info(request):
    if request.method=='PUT':
        try:
            data = request.data
            user_id = data['user_id'] = data['userid']
            pf = {"user_id": data['user_id'],
            "prefer_modern" : int(data['prefer'][0]),
            "prefer_natural" : int(data['prefer'][1]),
            "prefer_classic" : int(data['prefer'][2]),
            "prefer_industry" : int(data['prefer'][3]),
            "prefer_asia" : int(data['prefer'][4]),
            "prefer_provence" : int(data['prefer'][5]),
            "prefer_unique" : int(data['prefer'][6]),
                }
            del data['userid']
            del data['prefer']
            ac_object = Account.objects.filter(user_id=user_id)[0]
            pf_object = Prefer.objects.filter(user_id=user_id)[0]
            acSerializer= AccountSerializer(ac_object, data=data)
            pfSerializer = PreferSerializer(pf_object, data=pf)
            if acSerializer.is_valid(raise_exception=True) and pfSerializer.is_valid(raise_exception=True):
                acSerializer.save()
                pfSerializer.save()
            return JsonResponse({"code":200, "message":"Success 수정 성공"}, json_dumps_params={'ensure_ascii': False}, status=200)
        except Exception:
            return JsonResponse({"code":200, "message":"Fail 수정 실패"}, json_dumps_params={'ensure_ascii': False}, status=200)
    else:
        return JsonResponse({"code":200, "message":"잘못된 요청"}, json_dumps_params={'ensure_ascii': False}, status=200)