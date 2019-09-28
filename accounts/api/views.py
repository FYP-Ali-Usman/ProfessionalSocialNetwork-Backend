from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics,mixins, pagination
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from .serializers import UserRegisterSerializer
from .serializers import UserPublicSerializer
from .permissions import AnonPermissionOnly
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.api.permissions import IsOwnerOrReadOnly
import json

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
User = get_user_model()
def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
class AuthView(APIView):
    permission_classes =[AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail':'already authenticated'})
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        )
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        raise serializers.ValidationError('Invalid Credentials')


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes =[AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {'request':self.request}

class UserApiView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserPublicSerializer
    passed_id = None
    qs = None
    def get_queryset(self):
        request = self.request
        qs = User.objects
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs
    

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id',None) or self.passed_id
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id',None)
        json_data = {}
        bod = request.body
        if is_json(bod):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id',None)
        json_data = {}
        bod = request.body
        if is_json(bod):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        print(request.data)
        requested_id = request.data.get('id')
        passed_id = url_passed_id or new_passed_id or requested_id or None
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)


# class RegisterAPIView(APIView):
#     permission_classes =[permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail':'already authenticated or registered'})
#         data = request.data
#         username = data.get('username')
#         email = data.get('username')
#         password = data.get('password')
#         password2 = data.get('password2')
        

#         qs = User.objects.filter(
#             Q(username__iexact=username)|
#             Q(email__iexact=username)
#         )
#         if password != password2:
#             return Response({'password':'password must match'})
#         if qs.exists():
#             return Response({'detail':'user already exist'})
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user, request=request)
#             # return Response(response)
#             return Response({'detail':'iThanks for registering'})
#         return Response({'detail':'invalid request'})