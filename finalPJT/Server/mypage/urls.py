from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    # path('like/<user_id>', views.like_pie),
    # path('like/<user_id>', views.like_rader),
    # path('like/<user_id>', views.like_line),
    path('like/<user_id>', views.like_list),

]