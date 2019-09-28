from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.db import connection

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','email', 'first_name', 'last_name','message']
    def get_message(self, obj):
        return 'Your profile has been succesfully Updated'
    def validate_email(self, value):
        context = self.context
        request = context['request']
        qs2={'email':''}
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            qs2 = User.objects.get(email__iexact=value)
        if qs.exists() and qs2.email!=request.user.email :    
            raise serializers.ValidationError('Email alreday exists')
        return value
    def validate_username(self, value):
        context = self.context
        request = context['request']
        qs2={'username':''}
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            qs2 = User.objects.get(username__iexact=value)
        
        print(qs)
        if qs.exists() and qs2.username!=request.user.username :
            raise serializers.ValidationError('Username alreday exists')
        return value
    

    

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style = {'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','email', 'first_name', 'last_name','password','password2','token','token_response','message']
        extra_kwargs = {'password':{'write_only': True}}
    
    def get_message(self, obj):
        return 'Thanks for registering ! Your account has been succesfully creadted'
    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('Email alreday exists')
        return value
    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('Username alreday exists')
        return value
    def get_token_response(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        context = self.context
        request = context['request']
        print(request.user.is_authenticated)
        response = jwt_response_payload_handler(token, user, request=context['request'])
        return response
    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token
    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return data
    
    def create(self, validated_data):
        print(validated_data)
        user_obj = User(username = validated_data.get('username'), email = validated_data.get('email'), first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = True
        user_obj.save()
        return user_obj

