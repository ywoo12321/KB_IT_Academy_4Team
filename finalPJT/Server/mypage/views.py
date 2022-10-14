from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import  JsonResponse
import pandas as pd
import numpy as np
from lodgings.models import Lodging, Like
from datetime import datetime

def like_line(like_list):
    df = like_list.copy()
    dt_now = datetime.now().year * 12 + datetime.now().month
    df['total_time'] = df['like_date'].astype('datetime64').dt.year * 12 + df['like_date'].astype('datetime64').dt.month
    temp = df[(df['total_time'] < dt_now) & (df['total_time'] > dt_now-4)]
    top4 = np.sort(temp['total_time'].unique())[:4]
    dict_top4 = {}
    for i in top4:
        y = str(i // 12 if i % 12 != 0 else i // 12 - 1)
        m_temp = str(12 if i % 12 == 0 else i % 12)
        m = m_temp if len(m_temp) > 1 else '0'+m_temp
        
        temp_index = df[df['total_time']==i]['lodging_id_id'].value_counts().index
        lodging_object = Lodging.objects.filter(id__in=temp_index)
        dict_top4[y+"-"+m] = \
           [len(lodging_object.filter(tag=i)) for i in range(7)]
    return dict_top4

def like_rader(like_list):
    list_lod = list(like_list['lodging_id_id'].unique())
    list_lodging = [[i.lodging_name, i.lodging_address] for i in Lodging.objects.filter(id__in=list_lod)]
    df_lodging = pd.DataFrame(list_lodging, columns=['name', 'address'])
    temp = df_lodging.groupby(by='address').count().reindex()['name']
    result = dict(zip(temp.index, temp))
    return result

def like_pie(like_list):
    temp = like_list.groupby(by='lodging_id_id').count().reindex()['id']
    tag_dic = {
        0 : "Modern", 
        1 : "Natural", 
        2 : "Classic", 
        3 : "Industry", 
        4 : "Asia", 
        5 : "Provence", 
        6 : "Unique"
    }
    temp.index = list(map(lambda x : tag_dic[x], list(temp.index)))
    result = dict(zip(temp.index, temp))
    return result

@api_view(['GET'])
@permission_classes([AllowAny])
def like_chart(request, user_id):
    result = {}
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))
    result['line'] = like_line(user_like)
    result['pie'] = like_pie(user_like)
    result['rader'] = like_rader(user_like)
    return JsonResponse({'graph': result}, json_dumps_params={'ensure_ascii': False}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def like_list(request, user_id):
    user_like = pd.DataFrame(list(Like.objects.filter(user_id=user_id).values()))['lodging_id_id']
    return JsonResponse({'like': list(map(int, user_like.unique()))}, json_dumps_params={'ensure_ascii': False}, status=200)




