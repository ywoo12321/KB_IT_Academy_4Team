from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

# AbstractUser에 기본적으로 id와 password가 있음
class User(AbstractUser):
    
    # id(PK, index), username(로그인 id), pw(로그인 pw)
    # 유저 id
    user_id = models.CharField(max_length=10, unique=True, )
    # 유저 비밀번호
    password = models.CharField(max_length=10)
    # 유저 주소
    address = models.CharField(max_length=10)
    # 유저의 닉네임
    nickname = models.CharField(max_length=10)
    # USERNAME_FIELD = 'userId'    
    # Menu테이블과 1:n으로 연결 필요

# userName이 AbstractUser에 기본 제공되어 duplicate column name: userName Error 발생!
# createsuperuser 생성 시 default 값이 없으면 migrate가 잘 되어도 data가 들어가지 않는 이슈 발생.