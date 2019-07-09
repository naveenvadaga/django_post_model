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


class ReactGetPostSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    types = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )


class ReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    person = PersonSerializer()
    comment_at = serializers.DateTimeField()
    comment_content = serializers.CharField(max_length=100)
    reactions = ReactGetPostSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'person', 'comment_at', 'comment_content','reactions')


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    person = PersonSerializer()
    reactions = ReactGetPostSerializer()
    replies_count=serializers.IntegerField()
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'person', 'comment_at', 'comment_content','reactions', 'replies_count','replies')
        depth = 3


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ('__all__')


class ReactDeserializer(serializers.ModelSerializer):
    react_type = serializers.DictField(child=serializers.CharField())

    # count=serializers.IntegerField()
    class Meta:
        model = React
        fields = ('react_type')


# class



class GetPostSerializer(serializers.Serializer):
    id = serializers.CharField()
    posted_at = serializers.DateTimeField()
    post_content = serializers.CharField(max_length=100)
    person = PersonSerializer()
    reactions = ReactGetPostSerializer()
    comments = CommentSerializer(many=True)
    comments_count=serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'post_content', 'posted_at', 'reactions', 'person', 'comments')
