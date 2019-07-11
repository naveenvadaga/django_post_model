import pytest
from polls.models_utility_functions import *


@pytest.mark.django_db
class TestPersonModel:

    def test_my_user(self, person_fixture):
        persons_in_db = Person.objects.all().count()
        assert persons_in_db == 1


@pytest.mark.django_db
class TestPostModel:

    def test_post_creation(self, post_fixture):
        posts = Post.objects.all().count()
        assert posts == 1


@pytest.mark.django_db
class TestCommentModel:

    def test_comment_creation(self, comment_fixture):
        comments = Comment.objects.all()
        assert comments.count() == 1

    def test_reply_creation(self, reply_fixture):
        replys = Comment.objects.exclude(post_id=None).count()
        assert replys == 1


@pytest.mark.django_db
class TestReactModel:

    def test_react_to_post(self, react_to_post_fixture):
        reacts = React.objects.exclude(post_id=None).count()
        assert reacts == 1

    def test_react_to_comment(self, react_to_post_comment):
        reacts = React.objects.exclude(comment_id=None).count()
        assert reacts == 1

    def test_react_to_reply(self, react_to_reply):
        reacts = React.objects.exclude(comment_id=None).count()
        assert reacts == 1

    def test_react_to_same_post_with_same_reaction(self, react_to_same_post_same_reaction):
        reacts = React.objects.exclude(post_id=None).count()
        assert reacts == 0

    def test_react_to_same_post_with_different_reaction(self, react_to_same_post_with_different_reaction):
        reacts = React.objects.exclude(post_id=None).count()
        assert reacts == 1

    def test_react_to_same_comment_with_same_reaction(self, react_to_same_comment_same_reaction):
        reacts = React.objects.exclude(comment_id=None).count()
        assert reacts == 0

    def test_react_to_same_comment_with_different_reaction(self, react_to_same_comment_with_different_reaction):
        reacts = React.objects.exclude(comment_id=None).count()
        assert reacts == 1
