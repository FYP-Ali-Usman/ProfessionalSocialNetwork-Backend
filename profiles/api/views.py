from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, pagination
from django.shortcuts import get_object_or_404
import json
from rest_framework.parsers import FormParser,MultiPartParser

from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from profiles.models import Profile
from .serializers import ProfileSerializer,ProfileSerializer2

def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
# CLASS-------------------------------------------------------------------------
# class StatusListSearchApiView(APIView):
#     permission_classes = []
#     authentication_classes = []

#     def get(self, request, fromat=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs, many = True)
#         return Response(serializer.data)
# -------------------------------------------------------------------------------


# createModelMIxin --> POST data
# updateModelMixin --> PUT data
#  destroyMOdelMixin --> delete method
# class ApiPagination(pagination.PageNumberPagination):
    # page_size: 5


class ProfileApiView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProfileSerializer
    passed_id = None
    qs = None
    def get_queryset(self):
        request = self.request
        qs = Profile.objects
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
            obj = get_object_or_404(queryset, user_id=passed_id)
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



    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializers):
        serializers.save(user=self.request.user)

    

class ProfileApiView2(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProfileSerializer2
    passed_id = None
    qs = None
    parser_classes = (FormParser,MultiPartParser)
    def get_queryset(self):
        request = self.request
        qs = Profile.objects
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
    def perform_update(self, serializers):{
        serializers.save(user=self.request.user)
        }


    def patch(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id',None)
        json_data = {}
        bod = request.body
        if is_json(bod):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def delete(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id',None)
        json_data = {}
        bod = request.body
        if is_json(bod):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        return self.destroy(request, *args, **kwargs)
# ------------------------------------------------------------------------------------------------------------
# class StatusCreateApiView(generics.CreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
# -------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# class StatusDetailApiView(mixins.DestroyModelMixin , mixins.UpdateModelMixin , generics.RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     lookup_field = 'id'
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    # def get_object(self, *args, **kwargs):
    #     kwargs = self.kwargs
    #     kw_id = kwargs.get('id')
    #     return Status.objects.get(id=kw_id)
# --------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------
# class StatusUpdateApiView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     lookup_field = 'id'

# class StatusDeleteApiView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     lookup_field = 'id'
# ----------------------------------------------------------------------------------------------------------------