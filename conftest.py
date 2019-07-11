import pytest
from polls.models_utility_functions import *


@pytest.fixture()
def person_fixture():
    person = create("person1")
    return person


@pytest.fixture()
def post_fixture(person_fixture):
    post = create_post(person_fixture.id, "post_content")
    return post


@pytest.fixture()
def comment_fixture(person_fixture, post_fixture):
    comment = add_comment(post_fixture.id, person_fixture.id, "comment")
    return comment


@pytest.fixture()
def reply_fixture(comment_fixture, person_fixture):
    reply = reply_to_comment(comment_fixture.id, person_fixture.id, "reply")
    return reply


@pytest.fixture()
def react_to_post_fixture(person_fixture, post_fixture):
    react_to_post(person_fixture, post_fixture.id, "haha")


@pytest.fixture()
def react_to_post_comment(person_fixture, comment_fixture):
    react_to_comment(person_fixture, comment_fixture.id, "wow")


@pytest.fixture()
def react_to_reply(person_fixture, reply_fixture):
    react_to_comment(person_fixture, reply_fixture.id, "wow")


@pytest.fixture()
def react_to_same_post_same_reaction(person_fixture, post_fixture):
    react_to_post(person_fixture, post_fixture.id, "haha")
    react_to_post(person_fixture, post_fixture.id, "haha")


@pytest.fixture()
def react_to_same_post_with_different_reaction(person_fixture, post_fixture):
    react_to_post(person_fixture, post_fixture.id, "haha")
    react_to_post(person_fixture, post_fixture.id, "wow")


@pytest.fixture()
def react_to_same_comment_same_reaction(person_fixture, comment_fixture):
    react_to_comment(person_fixture, comment_fixture.id, "wow")
    react_to_comment(person_fixture, comment_fixture.id, "wow")


@pytest.fixture()
def react_to_same_comment_with_different_reaction(person_fixture, comment_fixture):
    react_to_comment(person_fixture, comment_fixture.id, "wow")
    react_to_comment(person_fixture, comment_fixture.id, "haha")
