from django.db import models
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from enum import Enum
from django.db.models import Count


# enum class

class ReactionChoice(Enum):
    Like = "like"
    Love = "love"
    Haha = "haha"
    Wow = "wow"
    Sad = "sad"
    Angry = "angry"


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.AutoField(primary_key=True)
    profilePicUrl = models.URLField(max_length=250, default="https://dummy.url.com/pic.png")

    @classmethod
    def create(cls, person_name):
        p = cls(name=person_name)
        p.save()
        return p


class React(models.Model):
    react_id = models.AutoField(primary_key=True)
    react_type = models.CharField(max_length=10, choices=[(reaction, reaction.value) for reaction in ReactionChoice])
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)

    @staticmethod
    def react_to_post(user_id, post_id, reaction_type):
        person_with_id = Person.objects.get(user_id=user_id)
        post_with_postId = Post.objects.get(post_id=post_id)

        reacted = React.objects.filter(Q(person=person_with_id) & Q(post=post_with_postId))
        if len(reacted) > 1:
            reacted = reacted[0]
            if reacted.react_type != reaction_type:
                reacted.react_type = reaction_type
                reacted.save()
                return reacted
            else:
                reacted.delete()
                return None
        else:
            react_created = React(react_type=reaction_type, person=person_with_id, post=post_with_postId)
            react_created.save()
            return react_created

    @staticmethod
    def react_to_comment(user_id, comment_id, reaction_type):
        person_with_id = Person.objects.get(user_id=user_id)
        comment_with_commentId = Comment.objects.get(comment_id=comment_id)

        reacted = React.objects.filter(Q(person=person_with_id) & Q(comment=comment_with_commentId))
        if len(reacted) > 1:
            reacted = reacted[0]
            if reacted.react_type != reaction_type:
                reacted.react_type = reaction_type
                reacted.save()
                return reacted
            else:
                reacted.delete()
                return None
        else:
            react_created = React(react_type=reaction_type, person=person_with_id, comment=comment_with_commentId)
            react_created.save()
            return react_created


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    comment_at = models.DateTimeField(auto_now_add=True, blank=True)
    comment_content = models.CharField(max_length=100)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    @staticmethod
    def add_comment(post_id, comment_user_id, comment_text):
        post_with_postId = Post.objects.get(post_id=post_id)
        person_with_id = Person.objects.get(user_id=comment_user_id)
        comment_created = Comment(post=post_with_postId, person=person_with_id, comment_content=comment_text)
        comment_created.save()
        return comment_created

    @staticmethod
    def reply_to_comment(comment_id, reply_user_id, reply_text):
        print("on 1")
        comment_with_commentId = Comment.objects.get(comment_id=comment_id)
        person_with_id = Person.objects.get(user_id=reply_user_id)
        print("on 2")

        if comment_with_commentId.reply == None:
            reply_created = Comment(person=person_with_id, comment_content=reply_text, reply=comment_with_commentId)
        else:
            comment_of_reply = Comment.objects.get(comment_id=comment_with_commentId.reply.comment_id)
            reply_created = Comment(person=person_with_id, comment_content=reply_text, reply=comment_of_reply)

        reply_created.save()
        return reply_created


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True, blank=True)
    post_content = models.CharField(max_length=100)

    @staticmethod
    def create_post(user_id, post_content):
        person_with_id = Person.objects.get(user_id=user_id)
        post_created = Post(person=person_with_id, post_content=post_content)
        post_created.save()
        return post_created

    @staticmethod
    def get_post(post_id):
        post_with_postId = Post.objects.get(post_id=post_id)
        posted_person = post_with_postId.person
        posted_at = post_with_postId.posted_at
        comments = Comment.objects.filter(post=post_with_postId)
        # reactions = React.objects.filter(post=post_with_postId)

        json_comments = []
        count = 1
        json_reply = []
        json_post_react = []
        json_comment_react = []

        post_react = React.objects.filter(post=post_with_postId)
        for react in post_react:
            json_post_react.append(react.react_type)

        for comment in comments:
            # replys = Comment.objects.filter(comment=comment.reply)
            replys = Comment.objects.filter(reply=comment)
            rcount = 1
            json_reply = []
            for reply in replys:
                reply_react = React.objects.filter(comment=reply)
                json_comment_react = []
                for reac in reply_react:
                    json_comment_react.append(reac.react_type)
                json_reply.append({
                    "comment_id": reply.comment_id,
                    "commenter": {
                        "user_id": reply.person.user_id,
                        "name": reply.person.name,
                        "profile_pic_url": reply.person.profilePicUrl
                    },
                    "commented_at": str(reply.comment_at),
                    "comment_content": reply.comment_content,
                    "reactions": {
                        "count": len(json_comment_react),
                        "type": json_comment_react
                    },

                })

            count += 1
            comment_react = React.objects.filter(comment=comment)
            json_comment_react = []
            for reac in comment_react:
                json_comment_react.append(reac.react_type)

            json_comments.append({
                "comment_id": comment.comment_id,
                "commenter": {
                    "user_id": comment.person.user_id,
                    "name": comment.person.name,
                    "profile_pic_url": comment.person.profilePicUrl
                },
                "commented_at": str(comment.comment_at),
                "comment_content": comment.comment_content,
                "reactions": {
                    "count": len(json_comment_react),
                    "type": json_comment_react
                },
                "replies_count": len(replys),
                "replies": json_reply

            })
        json_dict = {
            "post_id": post_id,
            "posted_by": {
                "name": posted_person.name,
                "user_id": posted_person.user_id,
                "profile_pic_url": posted_person.profilePicUrl

            },
            "posted_at": str(posted_at),
            "post_content": post_with_postId.post_content,
            "reactions": {
                "count": len(json_post_react),
                "type": json_post_react
            },
            "comments": json_comments,
            "comments_count": len(comments)

        }
        return (json.dumps(json_dict, indent=4, cls=DjangoJSONEncoder))


def get_user_posts(user_id):
    posts_with_userid = Post.objects.filter(person=Person.objects.get(user_id=user_id))
    user_post = []
    for post in posts_with_userid:
        user_post.append(Post.get_post(post.post_id))
    return user_post


def get_posts_with_more_positive_reactions():
    posts_with_more_positive_reaction = []
    reaction1 = Count('react', filter=Q(react__react_type=ReactionChoice.Haha.value))
    reaction2 = Count('react', filter=Q(react__react_type=ReactionChoice.Wow.value))
    reaction3 = Count('react', filter=Q(react__react_type=ReactionChoice.Like.value))
    reaction4 = Count('react', filter=Q(react__react_type=ReactionChoice.Love.value))
    reaction5 = Count('react', filter=Q(react__react_type=ReactionChoice.Angry.value))
    reaction6 = Count('react', filter=Q(react__react_type=ReactionChoice.Sad.value))
    posts = Post.objects.annotate(positive=reaction1 + reaction2 + reaction3 + reaction4 - reaction5 - reaction6)
    for post in posts:
        if post.positive > 0:
            posts_with_more_positive_reaction.append(post.post_id)
    return posts_with_more_positive_reaction




def get_posts_reacted_by_user(user_id):
    posts_reacted_by_user = []
    reacted_person = Person.objects.get(user_id=user_id)
    all_reactions = React.objects.filter(person=reacted_person)
    for react in all_reactions:
        if react.post != None:
            posts_reacted_by_user.append(Post.get_post(react.post.post_id))

    return posts_reacted_by_user


def get_reactions_to_post(post_id):
    reactions_to_posts = []
    reacted_post = Post.objects.get(post_id=post_id)
    reactions = React.objects.filter(post=reacted_post)
    for react in reactions:
        reactions_to_posts.append({
            "user_id": react.person.user_id,
            "name": react.person.name,
            "profile_pic": react.person.profilePicUrl,
            "reaction": react.react_type
        })
    return reactions_to_posts


def get_reaction_metrics(post_id):
    reaction_metrics = {}
    reacted_post = Post.objects.get(post_id=post_id)
    reactions = React.objects.filter(post=reacted_post)
    for react in reactions:
        reaction_type = react.react_type
        if reaction_type in reaction_metrics:
            reaction_metrics[reaction_type] += 1
        else:
            reaction_metrics[reaction_type] = 1

    return reaction_metrics


def get_total_reaction_count():
    return React.objects.exclude(post__isnull=True).count()


def get_replies_for_comment(comment_id):
    comment = Comment.objects.get(comment_id=comment_id)
    json_reply = []
    replys = Comment.objects.filter(reply=comment)
    rcount = 1
    for reply in replys:
        json_reply.append({
            "comment_id": reply.comment_id,
            "commenter": {
                "user_id": reply.person.user_id,
                "name": reply.person.name,
                "profile_pic_url": reply.person.profilePicUrl
            },
            "commented_at": str(reply.comment_at),
            "comment_content": reply.comment_content,

        })

    return json_reply


def delete_post(post_id):
    Post.objects.get(post_id=post_id).delete()
