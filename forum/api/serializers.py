from rest_framework import serializers
from forum.models import Article,Comment #,Tag
from accounts.api.serializers import UserPublicSerializer

# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'
    
#     def validate(self, data):
#         tag = data.get('tag')
#         if len(tag) > 50:
#             raise serializers.ValidationError('Tag name is too long')
#         return data

class ArticleSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(read_onlu=True)
    user = UserPublicSerializer(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
    def get_message(self, obj):
        return 'Your feed is succesfully submitted'
    def validate(self, data):
        title = data.get('title')
        if len(title) > 150:
            raise serializers.ValidationError('Title name is too long')
        return data

class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
    def get_message(self, obj):
        return 'Your comment is succesfully submitted'
    def validate(self, data):
        body = data.get('body')
        if body=="":
            raise serializers.ValidationError("Body can't be empty")
        return data
    