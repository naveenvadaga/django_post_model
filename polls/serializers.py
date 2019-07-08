from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('posted_at', 'post_content', 'id')


class PostDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('posted_at', 'post_content', 'person')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('username', 'date_joined', 'profilePicUrl', 'id')


class CommentDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment_at', 'comment_content', 'reply')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'person', 'post', 'comment_at', 'comment_content', 'reply')


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ('__all__')


class ReactDeserializer(serializers.ModelSerializer):
    # react_type = serializers.DictField(child=serializers.CharField())

    class Meta:
        model = React
        fields = ('react_type', 'post', 'comment')


class GetPostSerializer(serializers.Serializer):
    id = serializers.CharField()
    posted_at = serializers.DateTimeField()
    post_content = serializers.CharField(max_length=100)
    person = PersonSerializer()

    class Meta:
        model = Post
        fields = ('id', 'post_content', 'posted_at', 'person')
