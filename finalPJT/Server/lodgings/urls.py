from django.urls import path
from . import views

app_name = 'lodgings'
urlpatterns = [
    path('recommendation/<user_id>/', views.person_recom),
    path('recommendation/', views.basic_recom),
    path('<int:lodging_id>/', views.lodging_detail),
    path('search/<keyword>/', views.search_lodging),
    path('random/', views.random_maker),
    path('image/<theme>/<keyword>', views.image_response),
    path('like/<user_id>/<int:lodging_id>', views.like),
]