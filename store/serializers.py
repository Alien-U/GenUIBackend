from rest_framework import serializers
from .models import SavedLists,ListItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data.get('email', '')
        password = validated_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user


# What i changed
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'image_url', 'author', 'created_at']
        read_only_fields = ['author', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            url = str(obj.image.url)
            # Cloudinary URLs are already absolute; return as-is
            if url.startswith('http'):
                return url
            # Fallback: build absolute URL from request context
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class ListItemSerializer(serializers.ModelSerializer):
    post_content = serializers.CharField(source='post.content', read_only=True)
    post_image = serializers.SerializerMethodField()
    class Meta:
        model = ListItem
        fields = '__all__'

    def get_post_image(self, obj):
        if obj.post and obj.post.image:
            url = str(obj.post.image.url)
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
    
class ListsSerializer(serializers.ModelSerializer):
    items = ListItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    class Meta:
        model = SavedLists
        fields = '__all__'