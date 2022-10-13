from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import  JsonResponse, HttpResponse
import pandas as pd

from django.db.models import Count
from lodgings.models import Lodging, Like
from accounts.models import Prefer

def like_pie(request, lodging_id):
    pass

def like_rader(like_list, lodging_id):

    pass

def like_line(like_list, lodging_id):

    pass
@api_view(['GET'])
@permission_classes([AllowAny])
def like_list(request, user_id):
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))['lodging_id_id']
    return JsonResponse({'like': list(user_like)}, json_dumps_params={'ensure_ascii': False}, status=200)
    

    




