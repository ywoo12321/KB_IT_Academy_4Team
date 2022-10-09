from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Account, Prefer

@api_view(['GET'])
@permission_classes([AllowAny])
def user_test(request, user_id):
    print(user_id)
    user = get_object_or_404(Account, pk=user_id)
    print(user)
    return Response(user.nickname)

    
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