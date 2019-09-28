from rest_framework import serializers
from profiles.models import Profile
from accounts.api.serializers import UserPublicSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
    def get_message(self, obj):
        return 'Your profile has been succesfully Created'
    def validate(self, data):
        organization = data.get('organization')
        if len(organization) > 80:
            raise serializers.ValidationError('organization name is too long')
        about = data.get('about')
        if len(about) > 380:
            raise serializers.ValidationError('about details are too long')
        return data
        
class ProfileSerializer2(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
    def get_message(self, obj):
        return 'Your profile has been succesfully Updated'
    def validate(self, data):
        organization = data.get('organization')
        if len(organization) > 80:
            raise serializers.ValidationError('organization name is too long')
        about = data.get('about')
        if len(about) > 380:
            raise serializers.ValidationError('about details are too long')
        return data

