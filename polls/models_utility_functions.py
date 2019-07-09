from .models import *
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


# person

def create(person_name):
    p = Person(name=person_name)
    p.save()
    return p


# post
def create_post(user_id, post_content):
    person_with_id = Person.objects.get(user_id=user_id)
    post_created = Post(person=person_with_id, post_content=post_content)
    post_created.save()
    return post_created


def get_post(post_id):
    post = {}
    print(len(connection.queries))

    posted = Post.objects.filter(id=post_id).select_related('person')

    reactions_post = React.objects.filter(post_id=post_id).values('react_type')
    commented = Comment.objects.filter(post_id=post_id).select_related('person').prefetch_related(
        Prefetch('comment_set', to_attr='replies'))
    posted = posted[0]

    post["post_id"] = posted.id
    post["posted_by"] = posted.person
    post["posted_at"] = posted.posted_at.strftime("%m/%d/%Y, %H:%M:%S")
    post["post_content"] = posted.post_content

    json_comment_react = []
    for reac in reactions_post:
        json_comment_react.append(reac['react_type'])
    json_comment_react = set(json_comment_react)

    post["reactions"] = {
        "count": len(json_comment_react),
        "types": json_comment_react

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
        if int(a['comment_id']) in comment_reactions:
            comment_reactions[int(a['comment_id'])].add(a['react_type'])
        else:
            comment_reactions[int(a['comment_id'])] = {a['react_type']}

    reply_reactions = {}

    for a in reply_reaction:
        if a['comment_id'] in reply_reactions:
            reply_reactions[int(a['comment_id'])].add(a['react_type'])
        else:
            reply_reactions[int(a['comment_id'])] = {a['react_type']}

    for comment in commented:
        rep = []
        for reply in comment.replies:
            # print(reply.id)
            count = 0
            s = {}
            if reply.id in comment_reactions:
                count = len(reply_reactions[reply.id])
                s = reply_reactions[reply.id]

            rep.append({
                "comment_id": reply.id,
                "commenter": reply.person,
                "commented_at": reply.comment_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "comment_content": reply.comment_content,
                "reactions": {
                    "count": count,
                    "types": s
                }

            })
        ccount = 0
        cs = {}
        if comment.id in comment_reactions:
            ccount = len(comment_reactions[int(comment.id)])
            cs = comment_reactions[comment.id]

        post["comments"].append({
            "comment_id": comment.id,
            "commenter": comment.person,
            "commented_at": comment.comment_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "comment_content": comment.comment_content,
            "reactions": {
                "count": ccount,
                "types": cs
            },
            "replies_count": len(comment.replies),
            "replies": rep

        })

    post['comments_count'] = len(commented)
    print(len(connection.queries))

    return post


def get_user_posts(user_id):
    posts_with_userid = Post.objects.filter(person_id=user_id).values('id')
    user_post = []
    for post in posts_with_userid:
        user_post.append(get_post(post['id']))
    return user_post


def delete_post(post_id):
    Post.objects.get(id=post_id).delete()


# comments
def add_comment(post_id, comment_user_id, comment_text):
    post_with_postId = Post.objects.get(id=post_id)
    person_with_id = Person.objects.get(id=comment_user_id)
    comment_created = Comment(post=post_with_postId, person=person_with_id, comment_content=comment_text)
    comment_created.save()
    return comment_created


def reply_to_comment(comment_id, reply_user_id, reply_text):
    print("on 1")
    comment_with_commentId = Comment.objects.get(id=comment_id)
    person_with_id = Person.objects.get(id=reply_user_id)
    print("on 2")

    if comment_with_commentId.reply == None:
        reply_created = Comment(person=person_with_id, comment_content=reply_text, reply=comment_with_commentId)
    else:
        comment_of_reply = Comment.objects.get(id=comment_with_commentId.reply.id)
        reply_created = Comment(person=person_with_id, comment_content=reply_text, reply=comment_of_reply)

    reply_created.save()
    return reply_created


def get_replies_for_comment(comment_id):
    json_reply = []
    comments = Comment.objects.filter(id=comment_id).prefetch_related(
        Prefetch('comment_set', queryset=Comment.objects.select_related('person'), to_attr='replySet'))

    replys = comments[0].replySet
    for reply in replys:
        dict = {}
        dict['comment_id'] = reply.id
        dict['commenter'] = reply.person
        dict['commented_at'] = reply.comment_at.strftime("%Y/%m/%d, %H:%M:%S")
        dict['comment_content'] = reply.comment_content
        json_reply.append(dict)

    print(len(connection.queries))
    return json_reply


# react
def react_to_post(user_id, post_id, reaction_type):
    person_with_id = Person.objects.get(id=user_id)
    post_with_postId = Post.objects.get(id=post_id)
    try:
        reacted = React.objects.get(person=person_with_id, post=post_with_postId)
        if reacted.react_type != reaction_type:
            React.objects.filter(id=reacted.id).update(react_type=reaction_type)
        else:
            React.objects.get(id=reacted.id).delete()
            return None
    except ObjectDoesNotExist:
        react_created = React(react_type=reaction_type, person=person_with_id, post=post_with_postId)
        react_created.save()
        return react_created


def react_to_comment(user_id, comment_id, reaction_type):
    person_with_id = Person.objects.get(id=user_id)
    comment_with_commentId = Comment.objects.get(id=comment_id)
    try:
        reacted = React.objects.get(person=person_with_id, comment=comment_with_commentId)
        if reacted.react_type != reaction_type:
            React.objects.filter(id=reacted.id).update(react_type=reaction_type)
        else:
            React.objects.get(id=reacted.id).delete()
            return None
    except ObjectDoesNotExist:
        react_created = React(react_type=reaction_type, person=person_with_id, comment=comment_with_commentId)
        react_created.save()
        return react_created


def get_posts_with_more_positive_reactions():
    reaction1 = Count('react', filter=Q(react__react_type=ReactionChoice.Haha.value))
    reaction2 = Count('react', filter=Q(react__react_type=ReactionChoice.Wow.value))
    reaction3 = Count('react', filter=Q(react__react_type=ReactionChoice.Like.value))
    reaction4 = Count('react', filter=Q(react__react_type=ReactionChoice.Love.value))
    reaction5 = Count('react', filter=Q(react__react_type=ReactionChoice.Angry.value))
    reaction6 = Count('react', filter=Q(react__react_type=ReactionChoice.Sad.value))
    posts = Post.objects.annotate(
        positive=reaction1 + reaction2 + reaction3 + reaction4 - reaction5 - reaction6).filter(
        positive__gt=0 > 0).values('id')

    return posts


def get_posts_reacted_by_user(user_id):
    posts_reacted_by_users = []

    posts_reacted_by_user = React.objects.filter(person_id=user_id).values('id')
    for posts in posts_reacted_by_user:
        posts_reacted_by_users.append(posts['id'])

    return posts_reacted_by_users


def get_reactions_to_post(post_id):
    reactions_to_posts = []
    reactions = Post.objects.filter(id=post_id).prefetch_related(
        Prefetch('react_set', queryset=React.objects.select_related('person'), to_attr='reacts'))
    reactions = reactions[0].reacts
    for reaction in reactions:
        reactions_to_posts.append({
            "id": reaction.person_id,
            "username": reaction.person.username,
            "profilePicUrl": reaction.person.profilePicUrl,
            "reaction": reaction.react_type
        })

    return reactions_to_posts


def get_reaction_metrics(post_id):
    meterics = {}
    dict = React.objects.filter(post_id=post_id).values('react_type').annotate(react_count=Count('react_type'))
    for d in dict:
        meterics[d['react_type']] = d['react_count']

    return meterics


def get_total_reaction_count():
    return React.objects.exclude(post__isnull=True).count()
