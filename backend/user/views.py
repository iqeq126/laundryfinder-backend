import os, time, datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.parsers import JSONParser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import User
from .serializers import UserSerializer, RegisterSerializer#, UserInfoSerializer, UserUpdateSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import login, authenticate, logout
from rest_framework_simplejwt.views import TokenObtainPairView
# views.py
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_login_id, validate_password


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_login_id(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			#token = TokenObtainPairSerializer.get_token(user)
			#refresh_token = str(token)
			#access_token = str(token.access_token)

			login(request, user)
			return Response(
				serializer.data,
				status=status.HTTP_200_OK
			)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserMyView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class OnlyAuthenticatedUserView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = [JWTAuthentication]

	# 인가된 사용자의 정보 조회
	def get(self, request):
		user = request.user

		if not user:
			return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

		serialized_user = UserSerializer(user)
		return Response({"user_info": serialized_user.data}, status=status.HTTP_200_OK)
# TokenObtainPairView : urls.py에서 import했고, 토큰을 발급받기 위해 사용
"""
class SeasonTokenObtainPairView(TokenObtainPairView):
	# serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
	serializer_class = SeasonTokenObtainPairSerializer


# User 접근 권한 설정
class UserView(APIView):
	#permission_classes = [permissions.AllowAny]  # 누구나 view 접근 가능
	permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만 view 접근 가능
	# permission_classes = [permissions.IsAdminUser]     # admin 유저만 view 접근 가능
	# DONE 회원 정보 조회
	def get(self, request):
		data = User.objects.get(login_id=request.user.login_id)
		return Response(UserSerializer(data).data, status=status.HTTP_200_OK)

	# DONE 회원가입
	def post(self, request):
		user_serializer = UserSerializer(data=request.data)

		if user_serializer.is_valid():
			user_serializer.save()
			return Response(user_serializer.data, status=status.HTTP_200_OK)
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# DONE 회원 정보 수정
	def put(self, request):
		user = User.objects.get(login_id=request.user.login_id)
		user_serializer = UserSerializer(user, data=request.data, partial=True)

		if user_serializer.is_valid():
			user_serializer.save()
			return Response(user_serializer.data, status=status.HTTP_200_OK)
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# DONE 회원 탈퇴
	def delete(self, request):
		user = User.objects.get(login_id=request.user.login_id)
		if user:
			user.delete()
			return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
		return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)

# 로그인, 로그아웃
class UserAPIView(APIView):
	permission_classes = [permissions.AllowAny]

	# 로그인
	def post(self, request):
		login_id = request.data.get('login_id', '')
		password = request.data.get('password', '')

		# 변수 user에는 인증에 성공하면 user가 담기고, 인증 실패하면 None이 담기게 됨
		user = authenticate(request, login_id=login_id, password=password)

		if not user:
			return Response({"error": "존재하지 않는 계정 또는 일치하지 않는 비밀번호를 입력하셨습니다."})
		login(request, user)
		return Response({"msg": "login success!!"})

	# 로그아웃
	def delete(self, request):
		logout(request)
		return Response({"msg": "logout success!!"})

# 회원가입
class RegisterAPIView(APIView):
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			# jwt token 접근해주기
			token = TokenObtainPairSerializer.get_token(user)
			refresh_token = str(token)
			access_token = str(token.access_token)
			res = Response(
				{
					"user": serializer.data,
					"message": "register successs",
					"token": {
						"access": access_token,
						"refresh": refresh_token,
					},
				},
				status=status.HTTP_200_OK,
			)
			# 쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다.
			res.set_cookie("access", access_token, httponly=True)
			res.set_cookie("refresh", refresh_token, httponly=True)
			return res
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class AuthView(APIView):

	def post(self, request):
		user = authenticate(
			login_id=request.data.get("login_id"), password=request.data.get("password")
		)
		if user is not None:
			serializer = UserSerializer(user)
			token = TokenObtainPairSerializer.get_token(user)
			refresh_token = str(token)
			access_token = str(token.access_token)
			res = Response(
				{
					"user": serializer.data,
					"message": "login success",
					"token": {
						"access": access_token,
						"refresh": refresh_token,
					},
				},
				status=status.HTTP_200_OK,
			)
			return res
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
"""
"""
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		# Add custom claims
		token['user_name'] = user.user_name
		# ...

		return token

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer

@login_required
class UserDetailsView(RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated, )

	def get_object(self):
		return self.request.user


@login_required
class UserInfoView(RetrieveAPIView):
	serializer_class = UserInfoSerializer
	permission_classes = (AllowAny, )

	def get_queryset(self):
		return User.objects.all()

@login_required
class UserUpdateView(GenericAPIView):
	serializer_class = UserUpdateSerializer
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		user = self.request.user
		serializer = UserUpdateSerializer(user, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""