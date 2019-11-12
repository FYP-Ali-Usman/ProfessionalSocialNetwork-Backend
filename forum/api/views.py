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
from forum.models import Article,Comment
from .serializers import ArticleSerializer,CommentSerializer

def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid

class ArticleApiView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ArticleSerializer
    passed_id = None
    parser_classes = (FormParser,MultiPartParser)
    qs = None
    def get_queryset(self):
        request = self.request
        qs = Article.objects
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
            print(passed_id)
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



    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializers):
        serializers.save(user=self.request.user)

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

class ArticleDetailApiView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ArticleSerializer
    # queryset = Article.objects.all()
    def get_queryset(self):
        request = self.request
        passed_id2 = request.GET.get('id',None)
        qs = Article.objects
        if passed_id2 is not None:
            qs = qs.filter(user_id=passed_id2)
        return qs
    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     passed_id2 = request.GET.get('id',None)
    #     console.log(passed_id2)
    #     return Article.objects.filter(user_id=passed_id2)



class CommentApiView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CommentSerializer
    passed_id = None
    parser_classes = (FormParser,MultiPartParser)
    qs = None
    def get_queryset(self):
        request = self.request
        qs = Comment.objects
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
            print(passed_id)
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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializers):
        print(self.request.data)
        data=self.request.data
        art=Article.objects.filter(id=data['article_id'])
        serializers.save(user=self.request.user,article=art[0])

class CommentDetailApiView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CommentSerializer
    # queryset = Article.objects.all()
    def get_queryset(self):
        request = self.request
        passed_id2 = request.GET.get('id',None)
        qs = Comment.objects
        if passed_id2 is not None:
            qs = qs.filter(article_id=passed_id2)
        return qs

class ArticleDetailPubApiView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # pagination_class = ApiPagination
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ArticleSerializer
    # queryset = Article.objects.all()
    def get_queryset(self):
        request = self.request
        passed_id2 = request.GET.get('id',None)
        qs = Article.objects
        if passed_id2 is not None:
            qs = qs.filter(paperId=passed_id2)
        return qs
