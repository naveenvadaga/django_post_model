from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import *
from .serializers import *


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
        serializer = CommentSerializer(comments, many=True)
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
def get_post(request, pk):
    post = {}
    post_id=pk
    posted = Post.objects.filter(id=post_id).select_related('person')

    reactions_post = React.objects.filter(post_id=post_id).values('react_type')
    commented = Comment.objects.filter(post_id=1).select_related('person').prefetch_related(
        Prefetch('comment_set', to_attr='replies'))
    posted = posted[0]

    serializer=GetPostSerializer(posted)

    return Response(serializer.data)


    post["post_id"] = posted.id
    post["posted by"] = {"user_id": posted.person_id,

                         "name": posted.person.username,
                         "profile_pic_url": posted.person.profilePicUrl

                         }
    post["posted_at"] = posted.posted_at.strftime("%m/%d/%Y, %H:%M:%S")
    post["post_content"] = posted.post_content

    json_comment_react = []
    for reac in reactions_post:
        json_comment_react.append(reac['react_type'])
    json_comment_react = set(json_comment_react)

    post["reactions"] = {
        "count": len(json_comment_react),
        "type": json_comment_react

    }
    post["comments"] = []

    rep = []
    comment_id = []
    reply_id = []

    for comment in commented:
        comment_id.append(int(comment.id))
        for reply in comment.replies:
            reply_id.append(int(reply.id))

    comment_reaction = React.objects.filter(comment_id__in=comment_id).values('comment_id', 'react_type')
    reply_reaction = React.objects.filter(comment_id__in=reply_id).values('comment_id', 'react_type')
    comment_reactions = {}
    for a in comment_reaction:
        if a['comment_id'] in comment_reactions:
            comment_reactions[int(a['comment_id'])] = {a['react_type']}
        else:
            comment_reactions[int(a['comment_id'])].add(a['react_type'])

    reply_reactions = {}

    for a in reply_reaction:
        if a['comment_id'] in reply_reactions:
            reply_reactions[int(a['comment_id'])] = {a['react_type']}
        else:
            reply_reactions[int(a['comment_id'])].add(a['react_type'])

    for comment in commented:

        for reply in comment.replies:
            # print(reply.id)
            count = 0
            s = {}
            if reply.id in comment_reactions:
                count = len(reply_reactions[reply.id])
                s = reply_reactions[reply.id]

            rep.append({
                "comment_id": reply.id,
                "commenter": {
                    "user_id": reply.person_id,
                    "name": reply.person.username,
                    "profile_pic_url": reply.person.profilePicUrl
                },
                "commented_at": reply.comment_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "comment_content": reply.comment_content,
                "reactions": {
                    "count": count,
                    "type": s
                }

            })
        ccount = 0
        cs = {}
        if comment.id in comment_reactions:
            ccount = len(comment_reactions[reply.id])
            cs = comment_reactions[reply.id]

        post["comments"].append({
            "comments_id": comment.id,
            "commenter": {
                "user_id": comment.person_id,
                "name": comment.person.username,
                "profile_pic_url": comment.person.profilePicUrl
            },
            "commented_at": comment.comment_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "comment_content": comment.comment_content,
            "reactions": {
                "count": ccount,
                "type": cs
            },
            "replies_count": len(comment.replies),
            "replies": rep

        })




    post['comment_count'] = len(commented)
    print(len(connection.queries))
