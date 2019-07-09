from rest_framework import serializers
from .models import *


class listSerializer(serializers.ModelSerializer):
    list = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        fields = ('list',)


class countSerializer(serializers.Serializer):
    count = serializers.IntegerField()

    class Meta:
        fields = ('count',)


class dictSerializer(serializers.Serializer):
    list = serializers.DictField(
        child=serializers.CharField()
    )

    class Meta:
        fields = ('list',)


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


class ReactDeserializer(serializers.ModelSerializer):
    react_type = serializers.DictField(child=serializers.CharField())

    # count=serializers.IntegerField()
    class Meta:
        model = React
        fields = ('react_type')


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ('__all__')


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')


#### for get_ post ############
class ReactGetPostSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    types = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )


class ReplySerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(required=False)
    commenter = PersonSerializer()
    commented_at = serializers.DateTimeField()
    comment_content = serializers.CharField(max_length=100)
    reactions = ReactGetPostSerializer()

    class Meta:
        model = Comment
        fields = ('comment_id', 'commenter', 'commented_at', 'comment_content', 'reactions')


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(required=False)
    commenter = PersonSerializer()
    commented_at = serializers.DateTimeField()
    reactions = ReactGetPostSerializer()
    replies_count = serializers.IntegerField()
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ('comment_id', 'commenter', 'commented_at', 'comment_content', 'reactions', 'replies_count', 'replies')
        depth = 2


class GetPostSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField()
    posted_at = serializers.DateTimeField()
    post_content = serializers.CharField(max_length=100)
    posted_by = PersonSerializer()
    reactions = ReactGetPostSerializer()
    comments = CommentSerializer(many=True)
    comments_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('post_id', 'post_content', 'posted_at', 'reactions', 'posted_by', 'comments', 'comments_count')


##### end of get post ###############


class GetRepliesForPostSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(required=False)
    commenter = PersonSerializer()
    commented_at = serializers.DateTimeField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'commenter', 'commented_at', 'comment_content')


##### create post

class CreatePostDeserializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField()
    post_content = serializers.CharField()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ('post_content', 'person_id', 'id')


###

class AddCommentDeserializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()
    person_id = serializers.IntegerField()
    comment_content = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('id', 'comment_content', 'person_id', 'post_id')


###reply to comment

class ReplyToCommentDeserializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField()
    person_id = serializers.IntegerField()
    comment_content = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('id', 'comment_content', 'person_id', 'comment_id')


####react_to_post

class ReactToPost(serializers.ModelSerializer):
    person_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
    react_type = serializers.CharField()

    class Meta:
        model = React
        fields = ('id', 'react_type', 'person_id', 'post_id')


####react_to_comment

class ReactToComment(serializers.ModelSerializer):
    person_id = serializers.IntegerField()
    comment_id = serializers.IntegerField()
    react_type = serializers.CharField()

    class Meta:
        model = React
        fields = ('id', 'react_type', 'person_id', 'comment_id')


###
class ReactionsToPostSerializer(serializers.ModelSerializer):
    reaction = serializers.CharField()

    class Meta:
        model = Person
        fields = ('username', 'profilePicUrl', 'id', 'reaction')
