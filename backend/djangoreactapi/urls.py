"""djangoreactapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from crud import views as crud
# backend/djangoreactapi/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import ( TokenRefreshView )
from tag.views import TagViewSet
from user.views import UserMyView, UserRegister, UserLogin, UserLogout#, UserView, UserAPIView, SeasonTokenObtainPairView, OnlyAuthenticatedUserView, RegisterAPIView, AuthView#, MyTokenObtainPairView
from ptfile.views import LabelView
from ocr.views import OCRView

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# tag
router = routers.DefaultRouter()
router.register(r'post', TagViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path("api/", include("post.urls")),
    #path('api2/', include('ptfile.urls')),
    path('api2/label/', LabelView.as_view()),
    path('list/', crud.list),
    path('list2/', crud.list2),
    path('insert', crud.insertView.as_view()),
    path('detail/<int:product_code>', crud.detail),
    path('update', crud.update),
    path('delete', crud.delete),
    # path('clothes/', views.clothesAPI),
    path('map/', TemplateView.as_view(template_name='MapProduct.js')),
    path('clothes/', TemplateView.as_view(template_name='ClothesInformation.js')),
    path('tag/<str:tag_id>',TemplateView.as_view(template_name='TagInformation.js')), #
    path('backend/register', UserRegister.as_view(), name='register'),
    path('backend/login', UserLogin.as_view(), name='login'),
    path('backend/logout', UserLogout.as_view(), name='logout'),
    path('backend/token/user', UserMyView.as_view(), name='user'),
    path('ocr/', OCRView.as_view()),
    # Register
    # path("register/", RegisterAPIView.as_view()), #회원가입하기
    # path("auth/", AuthView.as_view()),  # 로그인하기
    # path('auth/refresh/', TokenRefreshView.as_view()),  # 토큰 재발급하기
    # 로그인 토큰(jwt) 관련
    path('backend/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #path('api/season/token/', SeasonTokenObtainPairView.as_view(), name='season_token'),
    #path('api/authonly/', OnlyAuthenticatedUserView.as_view()),
    # path('api/register', RegisterApi.as_view()),


    # 로그인 관련
    #path('user/', UserView.as_view()),
    #path('register/', RegisterAPIView.as_view()),
    #path('login/', UserAPIView.as_view()),
    #path('logout/', UserAPIView.as_view()),
    #path('auth/', AuthView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 토큰 관련
#path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
#path('api/register', RegisterApi.as_view()),
# 유저 관련
#path('login', LoginView.as_view(), name='rest_login'),
#path('registration', include('dj_rest_auth.registration.urls')),
#path('user/<pk>', user.UserInfoView.as_view()),
# URLs that require a user to be logged in with a valid session / token.
#path('user', user.UserDetailsView.as_view(), name='rest_user_details'),
#path('user/update', user.UserUpdateView.as_view()),
#path('password/change', PasswordChangeView.as_view(), name='rest_password_change'),
# 태그 관련
#tag/
#path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),#TemplateView를 상속받아 정의
#tag/tagname/
#path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),#ListView를 상속받아 정의