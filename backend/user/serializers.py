from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .validations import *
from .models import User


User = get_user_model()

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.login_id = clean_data['login_id']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	login_id = serializers.CharField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(login_id=clean_data['login_id'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'login_id')

class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

  def create(self, validated_data):
    login_id = validated_data.get('login_id')
    email = validated_data.get('email')
    password = validated_data.get('password')
    user = User(
      login_id=login_id,
      email=email
    )
    user.set_password(password)
    user.save()
    return user

# TokenObtain == Access Token 으로 생각하면 됨!
# 즉, 이곳에서 claim에 어떤 정보를 담고 싶은지에 대한 커스터마이징을 진행하면 됨!
class SeasonTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    # database에서 조회된 user의 정보가 user로 들어오게 된다. (요청한 user의 정보)
    def get_token(cls, user):
      # 가지고 온 user의 정보를 바탕으로 token을 생성한다.
        token = super().get_token(user)

        # 로그인한 사용자의 클레임 설정하기.
        token['username'] = user.username
        token['login_id'] = user.login_id
        token['email'] = user.email

        return token

#class SeasonTokenObtainPairView(TokenObtainPairView):
    # serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
#    serializer_class = SeasonTokenObtainPairSerializer
#class UserSerializer(serializers.ModelSerializer):
#  class Meta:
#    model = User
#    fields = '__all__'


"""
class SignupView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = SignupSirializer


class SignupSirializer(serializers.ModelSerializer):
  password = serializers.CharField(
    required=True,
    write_only=True,
  )
  class Meta:
    model = User
    fields = ('user_id', 'user_password', 'user_name')
    extra_kwargs={
      'user_password' : { 'write_only' : True},
    }

  def create(self, validated_data):
    user = User.objects.create_user(
      validated_data['user_id'],
      user_password = validated_data['user_password'],
      user_name=validated_data['user_name'],
      email=validated_data['email'],
    )
    return user

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['user_id', 'user_name', 'user_password']
    extra_kwargs = {
      'user_password': {'write_only': True}
    }
    def create(self, validated_data):
        password = validated_data.pop('user_password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

class UserInfoSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['user_id', 'user_name']


class UserUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['user_name']




class RegisterSerializer(RegisterSerializer):
  name = serializers.CharField(required=True, max_length=150)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data["user_name"] = self.validated_data.get("user_name", "")

    return data

  def validate(self, data):
    data = super().validate(data)
    if data["uesr_name"] == "":
      raise serializers.ValidationError("이름을 입력해주세요")

    try:
      User.objects.get(name=data["user_name"])
      raise serializers.ValidationError("이미 등록된 이름입니다.")
    except User.DoesNotExist:
      return data
"""