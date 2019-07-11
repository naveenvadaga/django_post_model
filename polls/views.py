from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
# from .models import *
from .serializers import *
from .models_utility_functions import *
from oauth2_provider.decorators import protected_resource
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrReadOnly
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
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
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
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
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
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
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def react_list(request, format=None):
    if request.method == 'GET':
        reacts = React.objects.all()
        serializer = ReactSerializer(reacts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        deserializer = ReactDeserializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save(person=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get'])
@protected_resource(scopes=['read'])
def get_post_(request, post_id):
    serializer = GetPostSerializer(get_post(post_id))
    return Response(serializer.data)


@api_view(['Get'])
@protected_resource(scopes=['read'])
def get_post_user_view(request):
    serializer = GetPostSerializer(get_user_posts(request.user), many=True)
    return Response(serializer.data)


@api_view(['Get'])
@protected_resource(scopes=['read'])
def get_replies_for_comment_view(request, comment_id):
    serializer = GetRepliesForPostSerializer(get_replies_for_comment(comment_id), many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def create_post_view(request):
    print(request.data)
    serializer = CreatePostDeserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def add_comment_to_post(request):
    serializer = AddCommentDeserializer(data=request.data)
    if serializer.is_valid():
        add_comment(request.data['post_id'], request.user, request.data['comment_content'])
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def reply_to_comment_view(request):
    serializer = ReplyToCommentDeserializer(data=request.data)
    if serializer.is_valid():
        reply_to_comment(request.data['comment_id'], request.user, request.data['comment_content'])
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def react_to_post_view(request):
    serializer = ReactToPost(data=request.data)
    if serializer.is_valid():
        react_to_post(request.user, request.data['post_id'], request.data['react_type'])
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def react_to_comment_view(request):
    serializer = ReactToComment(data=request.data)
    if serializer.is_valid():
        react_to_comment(request.user, request.data['comment_id'], request.data['react_type'])
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@protected_resource(scopes=['read'])
def get_posts_with_more_positive_reactions_view(request):
    serializer = ListSerializer({"list": get_posts_with_more_positive_reactions()})
    return Response(serializer.data)


@api_view(['GET'])
@protected_resource(scopes=['read'])
def get_posts_reacted_by_user_view(request):
    print(request.user)
    serializer = ListSerializer({"list": get_posts_reacted_by_user(request.user)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((TokenHasReadWriteScope,))
def get_reactions_to_post_view(request, post_id):
    serializer = ReactionsToPostSerializer(get_reactions_to_post(post_id), many=True)
    return Response(serializer.data)


@api_view(['GET'])
@protected_resource(scopes=['read'])
def get_reaction_metrics_view(request, post_id):
    serializer = DictSerializer({"dist": get_reaction_metrics(post_id)})
    return Response(serializer.data)


@api_view(['GET'])
@protected_resource(scopes=['read'])
def get_total_reaction_count_view(request):
    serializer = CountSerializer({"count": get_total_reaction_count()})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, TokenHasReadWriteScope))
def delete_post_view(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST' and "post_id" in request.data:
        post_id = request.data["post_id"]
        delete_post(post_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
