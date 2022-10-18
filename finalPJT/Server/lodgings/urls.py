from django.urls import path
from . import views

app_name = 'lodgings'
urlpatterns = [
    path('recommendation/<user_id>/', views.person_recom),
    path('recommendation/', views.basic_recom),
    path('<int:lodging_id>/', views.lodging_detail),
    path('sublodging/<int:lodging_id>/', views.sub_lodging),
    path('search/<keyward>/', views.search_lodging),
    path('image/<lodging_id>/', views.image_response),
]