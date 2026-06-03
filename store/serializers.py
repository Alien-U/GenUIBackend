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
    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'created_at']
        read_only_fields = ['author'] 


class ListItemSerializer(serializers.ModelSerializer):
    post_content = serializers.CharField(source='post.content', read_only=True)
    post_image = serializers.ImageField(source='post.image', read_only=True)
    class Meta:
        model = ListItem
        fields = '__all__'
    
class ListsSerializer(serializers.ModelSerializer):
    items = ListItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    class Meta:
        model = SavedLists
        fields = '__all__'