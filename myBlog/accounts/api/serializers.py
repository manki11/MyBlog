from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.authtoken.models import Token

User = get_user_model()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name'
        ]

    def get_name(self, obj):
        return str(obj.first_name + ' ' + obj.last_name)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {"password":
                            {'write_only': True}
                        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError('This email is already registered')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(allow_blank=True, read_only=True)


    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token'
        ]
        extra_kwargs = {"password":
                            {'write_only': True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data['password']

        if not email and not username:
            raise serializers.ValidationError("A username or email must be entered")
        user = User.objects.filter(
            Q(username=username),
            Q(email=email)
        ).distinct()

        user=user.exclude(email__isnull=True).exclude(email__iexact='')

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Given password is incorrect")

        token = Token.objects.filter(user=user_obj).first()

        data['token']=token

        return data
