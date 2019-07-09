from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import *
from .serializers import *
from .models_utility_functions import *


@api_view(['GET', 'POST'])
def post_list(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostDeserializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(person=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def person_list(request, format=None):
    if request.method == 'GET':
        posts = Person.objects.all()
        serializer = PersonSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get', 'Post'])
def comment_list(request, format=None):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        deserializers = CommentDeserializer(data=request.data)
        if deserializers.is_valid():
            deserializers.save(person=request.user)
            return Response(deserializers.data, status=status.HTTP_201_CREATED)
        return Response(deserializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get', 'Post'])
def react_list(request, format=None):
    if request.method == 'GET':
        reacts = React.objects.all()
        serializer = ReactSerializer(reacts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        deserializer = ReactDeserializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save(person=request.user)
            return Response(deserializer.data, status=status.HTTP_201_CREATED)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get'])
def get_post_(request, pk):
    serializer = GetPostSerializer(get_post(pk))
    return Response(serializer.data)


@api_view(['Get'])
def get_post_user_view(request, pk):
    serializer = GetPostSerializer(get_user_posts(pk), many=True)
    return Response(serializer.data)


@api_view(['Get'])
def get_replies_for_comment_view(request, post_id):
    serializer = GetRepliesForPostSerializer(get_replies_for_comment(post_id), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_post_view(request):
    print(request.data)
    serializer = CreatePostDeserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def add_comment_to_post(request):
    serializer = AddCommentDeserializer(data=request.data)
    if serializer.is_valid():
        add_comment(request.data['post_id'], request.data['person_id'], request.data['comment_content'])
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def reply_to_comment_view(request):
    serializer = ReplyToCommentDeserializer(data=request.data)
    if serializer.is_valid():
        reply_to_comment(request.data['comment_id'], request.data['person_id'], request.data['comment_content'])
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def react_to_post_view(request):
    serializer = ReactToPost(data=request.data)
    if serializer.is_valid():
        react_to_post(request.data['person_id'], request.data['post_id'], request.data['react_type'])
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def react_to_comment_view(request):
    serializer = ReactToComment(data=request.data)
    if serializer.is_valid():
        react_to_comment(request.data['person_id'], request.data['comment_id'], request.data['react_type'])
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_posts_with_more_positive_reactions_view(request):
    serializer = listSerializer({"list": get_posts_with_more_positive_reactions()})
    return Response(serializer.data)


@api_view(['GET'])
def get_posts_reacted_by_user_view(request, user_id):
    serializer = listSerializer({"list": get_posts_reacted_by_user(user_id)})
    return Response(serializer.data)


@api_view(['GET'])
def get_reactions_to_post_view(request, post_id):
    serializer = ReactionsToPostSerializer(get_reactions_to_post(post_id), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reaction_metrics_view(request, post_id):
    serializer = dictSerializer({"list": get_reaction_metrics(post_id)})
    return Response(serializer.data)


@api_view(['GET'])
def get_total_reaction_count_view(request):
    serializer = countSerializer({"count": get_total_reaction_count()})
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExixts:
        return Response(status=status.HTTP_404_NOT_FOUND)
