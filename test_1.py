import pytest
from polls.models_utility_functions import *
from django.core.exceptions import ObjectDoesNotExist
from polls.models import *


@pytest.mark.django_db
class TestPersonModel:

    def test_my_user(self, person_fixture):
        assert person_fixture is not None
        assert person_fixture.username == "person1"


@pytest.mark.django_db
class TestPostModel:

    def test_post_creation(self, person_fixture):
        content = "post content"
        total_post_count_before_creations = Post.objects.all().count()
        post = create_post(person_fixture.id, content)
        total_post_count_after_creations = Post.objects.all().count()
        assert total_post_count_after_creations == total_post_count_before_creations + 1
        assert post.person == person_fixture
        assert post.post_content == content

    def test_post_creation_without_user(self, person_fixture):
        content = "content"
        person_id = person_fixture.id
        person_fixture.delete()
        with pytest.raises(ObjectDoesNotExist):
            post = create_post(person_id, content)

    def test_delete_post(self, post_fixture):
        id = post_fixture.id
        assert post_fixture is not None
        post_fixture.delete()
        with pytest.raises(ObjectDoesNotExist):
            Post.objects.get(pk=id)

    def test_comment_for_post_creation(self, person_fixture, post_fixture):
        post_id = post_fixture.id
        content = "comment content"
        comment_count_for_post_before_creation = Comment.objects.filter(post_id=post_id).count()
        comment = add_comment(post_fixture.id, person_fixture.id, content)
        comment_count_for_post_after_creation = Comment.objects.filter(post_id=post_id).count()
        assert comment_count_for_post_before_creation + 1 == comment_count_for_post_after_creation
        assert comment.comment_content == content
        assert comment.post_id == post_fixture.id

    def test_multiple_comments_for_post_creation(self, person_fixture, post_fixture):
        post_id = post_fixture.id
        content1 = "comment 1"
        content2 = "comment 2"
        content3 = "comment 3"
        comment_count_for_post_before_creation = Comment.objects.filter(post_id=post_id).count()
        comment1 = add_comment(post_fixture.id, person_fixture.id, content1)
        comment2 = add_comment(post_fixture.id, person_fixture.id, content2)
        comment3 = add_comment(post_fixture.id, person_fixture.id, content3)
        comment_count_for_post_after_creation = Comment.objects.filter(post_id=post_id).count()
        assert comment_count_for_post_before_creation + 3 == comment_count_for_post_after_creation
        assert Comment.objects.get(post_id=post_id, pk=comment1.id).comment_content == content1
        assert Comment.objects.get(post_id=post_id, pk=comment2.id).comment_content == content2
        assert Comment.objects.get(post_id=post_id, pk=comment3.id).comment_content == content3

    def test_reactions_count(self, persons_fixture, posts_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        post1 = posts_fixture[0].id
        post2 = posts_fixture[1].id
        post3 = posts_fixture[2].id
        react_count_for_post_before_creation = get_total_reaction_count()
        react_to_post(person1, post1, react_type1)
        react_to_post(person2, post2, react_type2)
        react_to_post(person3, post3, react_type3)
        react_count_for_post_after_creation = get_total_reaction_count()
        assert react_count_for_post_before_creation + 3 == react_count_for_post_after_creation

    def test_posts_with_positive_reactions(self, persons_fixture, posts_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        react_type4 = "love"
        react_type5 = "sad"
        react_type6 = "angry"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        post1 = posts_fixture[0].id
        post2 = posts_fixture[1].id
        post3 = posts_fixture[2].id
        react_to_post(person1, post1, react_type1)
        react_to_post(person2, post1, react_type2)
        react_to_post(person3, post1, react_type3)
        react_to_post(person1, post2, react_type5)
        react_to_post(person2, post2, react_type5)
        react_to_post(person3, post2, react_type3)
        react_to_post(person1, post3, react_type5)
        react_to_post(person2, post3, react_type1)
        react_to_post(person3, post3, react_type3)
        posts_with_more_positive_reactions = get_posts_with_more_positive_reactions()
        posts_with_more_positive_reactions = set([a['id'] for a in posts_with_more_positive_reactions])
        posts = set([post1, post3])
        assert posts_with_more_positive_reactions == posts

    def test_posts_with_positive_reactions_edge_cases(self, persons_fixture, posts_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        react_type4 = "love"
        react_type5 = "sad"
        react_type6 = "angry"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        post1 = posts_fixture[0].id
        post2 = posts_fixture[1].id
        post3 = posts_fixture[2].id
        react_to_post(person1, post1, react_type5)
        react_to_post(person2, post1, react_type2)
        react_to_post(person3, post1, react_type6)
        react_to_post(person1, post2, react_type5)
        react_to_post(person2, post2, react_type5)
        react_to_post(person3, post2, react_type3)
        react_to_post(person1, post3, react_type5)
        react_to_post(person2, post3, react_type6)
        react_to_post(person3, post3, react_type4)
        posts_with_more_positive_reactions = get_posts_with_more_positive_reactions()
        posts_with_more_positive_reactions = set([a['id'] for a in posts_with_more_positive_reactions])
        posts = set([])
        assert posts_with_more_positive_reactions == posts

    def test_get_post_post(self, post_setup):
        post = post_setup[0]
        person_posted = post_setup[1]
        post_reactions = set()
        post_reactions.add(post_setup[2].react_type)
        post_reactions.add(post_setup[3].react_type)
        post_reactions.add(post_setup[4].react_type)
        post_test_data = get_post(post.id)
        assert post_test_data["post_id"] == post.id
        assert post_test_data["posted_by"] == person_posted
        assert post_test_data["posted_at"] == post.posted_at.strftime("%m/%d/%Y, %H:%M:%S")
        assert post_test_data["post_content"] == post.post_content
        assert post_test_data["reactions"] == {
            "count": len(post_reactions),
            "types": post_reactions
        }

    def test_get_post_comments(self, post_setup):
        comment = post_setup[8]
        person_commented = post_setup[9]
        comment_reactions = set()
        comment_reactions.add(post_setup[10].react_type)
        comment_reactions.add(post_setup[11].react_type)
        comment_reactions.add(post_setup[12].react_type)
        comment_test_data = get_post(post_setup[0].id)["comments"][0]

        assert comment_test_data["comment_id"] == comment.id
        assert comment_test_data["commenter"] == person_commented
        assert comment_test_data["commented_at"] == comment.comment_at.strftime("%m/%d/%Y, %H:%M:%S")
        assert comment_test_data["comment_content"] == comment.comment_content
        assert comment_test_data["reactions"] == {
            "count": len(comment_reactions),
            "types": comment_reactions
        }

    def test_get_post_replies(self, post_setup):
        reply1_for_comment = post_setup[13]
        reply1_person = post_setup[14]
        reply2_for_comment = post_setup[15]
        reply2_person = post_setup[16]
        reply1_reactions = set()
        reply2_reactions = set()
        reply1_reactions.add(post_setup[17].react_type)
        reply2_reactions.add(post_setup[18].react_type)
        reply1_test_data = get_post(post_setup[0].id)["comments"][0]["replies"][0]
        reply2_test_data = get_post(post_setup[0].id)["comments"][0]["replies"][1]
        assert reply1_test_data["comment_id"] == reply1_for_comment.id
        assert reply1_test_data["comment_id"] == reply1_for_comment.id
        assert reply1_test_data["commenter"] == reply1_person
        assert reply1_test_data["comment_content"] == reply1_for_comment.comment_content
        assert reply2_test_data["comment_id"] == reply2_for_comment.id
        assert reply2_test_data["comment_id"] == reply2_for_comment.id
        assert reply2_test_data["commenter"] == reply2_person
        assert reply2_test_data["comment_content"] == reply2_for_comment.comment_content


@pytest.mark.django_db
class TestCommentModel:

    def test_comment_creation(self, person_fixture, post_fixture):
        content = "comment content"
        total_comment_count_before_creations = Comment.objects.filter(reply_id=None).count()
        comment = add_comment(post_fixture.id, person_fixture.id, content)
        total_comment_count_after_creations = Comment.objects.filter(reply_id=None).count()
        assert total_comment_count_before_creations + 1 == total_comment_count_after_creations
        assert comment.person == person_fixture
        assert comment.post == post_fixture
        assert comment.comment_content == content

    def test_reply_creation(self, comment_fixture, person_fixture):
        content = "reply content"
        total_reply_count_before_creations = Comment.objects.filter(post_id=None).count()
        reply = reply_to_comment(comment_fixture.id, person_fixture.id, content)
        total_reply_count_after_creations = Comment.objects.filter(post_id=None).count()
        assert total_reply_count_before_creations + 1 == total_reply_count_after_creations
        assert reply.person == person_fixture
        assert reply.reply == comment_fixture
        assert reply.comment_content == content

    def test_reply_to_reply_creation(self, person_fixture, reply_fixture):
        content = "reply to reply"
        comment_for_reply_id = reply_fixture.reply
        total_replies_for_comment_before_creation = Comment.objects.filter(reply_id=comment_for_reply_id.id).count()
        reply = reply_to_comment(reply_fixture.id, person_fixture.id, content)
        total_replies_for_comment_after_creation = Comment.objects.filter(reply_id=comment_for_reply_id.id).count()
        assert total_replies_for_comment_before_creation + 1 == total_replies_for_comment_after_creation

    def test_replies_comment(self, person_fixture, comment_fixture):
        comment_id = comment_fixture.id
        content1 = "comment 1"
        content2 = "comment 2"
        content3 = "comment 3"
        replies_count_for_comment__before_creation = Comment.objects.filter(reply_id=comment_id).count()
        reply1 = reply_to_comment(comment_fixture.id, person_fixture.id, content1)
        reply2 = reply_to_comment(comment_fixture.id, person_fixture.id, content2)
        reply3 = reply_to_comment(comment_fixture.id, person_fixture.id, content3)
        replies_count_for_comment_after_creation = Comment.objects.filter(reply_id=comment_id).count()
        assert replies_count_for_comment__before_creation + 3 == replies_count_for_comment_after_creation
        assert Comment.objects.get(reply_id=comment_id, pk=reply1.id).comment_content == content1
        assert Comment.objects.get(reply_id=comment_id, pk=reply2.id).comment_content == content2
        assert Comment.objects.get(reply_id=comment_id, pk=reply3.id).comment_content == content3


@pytest.mark.django_db
class TestReactModel:

    def test_react_to_post(self, person_fixture, post_fixture):
        react_type = "haha"
        count_reacts_before_creaction = React.objects.exclude(post_id=None).count()
        react = react_to_post(person_fixture, post_fixture.id, react_type)
        count_reacts_after_creation = React.objects.exclude(post_id=None).count()
        assert count_reacts_before_creaction + 1 == count_reacts_after_creation
        assert react.react_type == react_type
        assert react.person == person_fixture

    def test_react_to_comment(self, person_fixture, comment_fixture):
        react_type = "wow"
        count_reacts_to_comments_before_creation = React.objects.exclude(comment_id=None).count()
        react = react_to_comment(person_fixture, comment_fixture.id, react_type)
        count_reacts_to_comments_after_creation = React.objects.exclude(comment_id=None).count()
        assert count_reacts_to_comments_before_creation + 1 == count_reacts_to_comments_after_creation
        assert react.person == person_fixture

    def test_react_to_reply(self, person_fixture, reply_fixture):
        react_type = "wow"
        count_react_to_reply_before_creation = React.objects.exclude(comment_id=None).count()
        react = react_to_comment(person_fixture, reply_fixture.id, react_type)
        count_react_to_reply_after_creation = React.objects.exclude(comment_id=None).count()
        assert count_react_to_reply_before_creation + 1 == count_react_to_reply_after_creation
        assert react.person == person_fixture
        assert react.react_type == react_type

    def test_react_to_same_post_with_same_reaction(self, person_fixture, post_fixture):
        react_type = "haha"
        count_react_to_post_before_creation = React.objects.filter(post_id=post_fixture.id).count()
        react = react_to_post(person_fixture, post_fixture.id, react_type)
        count_react_to_post_after_creation_first_reaction = React.objects.filter(post_id=post_fixture.id).count()
        assert count_react_to_post_before_creation + 1 == count_react_to_post_after_creation_first_reaction
        # react to same post with same reaction
        react = react_to_post(person_fixture, post_fixture.id, react_type)
        count_react_to_post_after_creation_second_reaction = React.objects.filter(post_id=post_fixture.id).count()
        assert count_react_to_post_before_creation == count_react_to_post_after_creation_second_reaction

    def test_react_to_same_post_with_different_reaction(self, person_fixture, post_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        count_react_to_post_before_creation = React.objects.filter(post_id=post_fixture.id).count()
        react = react_to_post(person_fixture, post_fixture.id, react_type1)
        count_react_to_post_after_creation_first_reaction = React.objects.filter(post_id=post_fixture.id).count()
        assert count_react_to_post_before_creation + 1 == count_react_to_post_after_creation_first_reaction
        # react to same post with different reaction
        react = react_to_post(person_fixture, post_fixture.id, react_type2)
        count_react_to_post_after_creation_second_reaction = React.objects.filter(post_id=post_fixture.id).count()
        assert count_react_to_post_before_creation + 1 == count_react_to_post_after_creation_second_reaction

    def test_react_to_same_comment_with_same_reaction(self, person_fixture, comment_fixture):
        react_type = "haha"
        count_react_to_comment_before_creation = React.objects.filter(comment_id=comment_fixture.id).count()
        react = react_to_comment(person_fixture, comment_fixture.id, react_type)
        count_react_to_comment_after_creation_first_reaction = React.objects.filter(
            comment_id=comment_fixture.id).count()
        assert count_react_to_comment_before_creation + 1 == count_react_to_comment_after_creation_first_reaction
        # react to same comment with same reaction
        react = react_to_comment(person_fixture, comment_fixture.id, react_type)
        count_react_to_comment_after_creation_second_reaction = React.objects.filter(
            comment_id=comment_fixture.id).count()
        assert count_react_to_comment_before_creation == count_react_to_comment_after_creation_second_reaction

    def test_react_to_same_comment_with_different_reaction(self, person_fixture, comment_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        count_react_to_comment_before_creation = React.objects.filter(comment_id=comment_fixture.id).count()
        react = react_to_comment(person_fixture, comment_fixture.id, react_type1)
        count_react_to_comment_after_creation_first_reaction = React.objects.filter(
            comment_id=comment_fixture.id).count()
        assert count_react_to_comment_before_creation + 1 == count_react_to_comment_after_creation_first_reaction
        # react to same post with different reaction
        react = react_to_comment(person_fixture, comment_fixture.id, react_type2)
        count_react_to_comment_after_creation_second_reaction = React.objects.filter(
            comment_id=comment_fixture.id).count()
        assert count_react_to_comment_before_creation + 1 == count_react_to_comment_after_creation_second_reaction

    def test_reactions_to_posts(self, persons_fixture, post_fixture):
        post_id = post_fixture.id
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        react_count_for_post_before_creation = React.objects.filter(post_id=post_id).count()
        react1 = react_to_post(person1, post_id, react_type1)
        react2 = react_to_post(person2, post_id, react_type2)
        react3 = react_to_post(person3, post_id, react_type3)
        react_count_for_post_after_creation = React.objects.filter(post_id=post_id).count()
        assert react_count_for_post_before_creation + 3 == react_count_for_post_after_creation
        assert React.objects.get(post_id=post_id, pk=react1.id).react_type == react_type1
        assert React.objects.get(post_id=post_id, pk=react2.id).react_type == react_type2
        assert React.objects.get(post_id=post_id, pk=react3.id).react_type == react_type3

    def test_reactions_to_comments(self, persons_fixture, comment_fixture):
        comment_id = comment_fixture.id
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        react_count_for_comment_before_creation = React.objects.filter(comment_id=comment_id).count()
        react1 = react_to_comment(person1, comment_id, react_type1)
        react2 = react_to_comment(person2, comment_id, react_type2)
        react3 = react_to_comment(person3, comment_id, react_type3)
        react_count_for_comment_after_creation = React.objects.filter(comment_id=comment_id).count()
        assert react_count_for_comment_before_creation + 3 == react_count_for_comment_after_creation
        assert React.objects.get(comment_id=comment_id, pk=react1.id).react_type == react_type1
        assert React.objects.get(comment_id=comment_id, pk=react2.id).react_type == react_type2
        assert React.objects.get(comment_id=comment_id, pk=react3.id).react_type == react_type3

    def test_reactions_count(self, persons_fixture, post_fixture):
        post_id = post_fixture.id
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        react_count_for_post_before_creation = React.objects.filter(post_id=post_id).count()
        react_to_post(person1, post_id, react_type1)
        react_to_post(person2, post_id, react_type2)
        react_to_post(person3, post_id, react_type3)
        react_count_for_post_after_creation = React.objects.filter(post_id=post_id).count()
        assert react_count_for_post_before_creation + 3 == react_count_for_post_after_creation

    def test_posts_reacted_by_user(self, person_fixture, posts_fixture):
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        react1 = react_to_post(person_fixture, posts_fixture[0].id, react_type1)
        react2 = react_to_post(person_fixture, posts_fixture[1].id, react_type2)
        react3 = react_to_post(person_fixture, posts_fixture[2].id, react_type3)
        posts_reacted_by_user = get_posts_reacted_by_user(person_fixture.id)
        posts = []
        posts.append(react1.id)
        posts.append(react2.id)
        posts.append(react3.id)
        posts = set(posts)
        posts_reacted_by_user = set(posts_reacted_by_user)
        assert posts == posts_reacted_by_user

    def test_reaction_metrics(self, post_fixture, persons_fixture, person_fixture):
        post_id = post_fixture.id
        react_type1 = "haha"
        react_type2 = "wow"
        react_type3 = "like"
        person1 = persons_fixture[0]
        person2 = persons_fixture[1]
        person3 = persons_fixture[2]
        person4 = person_fixture
        react1 = react_to_post(person1, post_id, react_type1)
        react2 = react_to_post(person2, post_id, react_type2)
        react3 = react_to_post(person3, post_id, react_type3)
        react4 = react_to_post(person4, post_id, react_type1)
        dict = get_reaction_metrics(post_id)
        assert dict[react_type1] == 2
        assert dict[react_type2] == 1
        assert dict[react_type3] == 1
