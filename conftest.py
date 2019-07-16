import pytest
from polls.models_utility_functions import *


@pytest.fixture()
def person_fixture():
    person = create("person1")
    return person


@pytest.fixture()
def persons_fixture():
    person1 = create("person")
    person2 = create("person2")
    person3 = create("person3")
    return person1, person2, person3


@pytest.fixture()
def post_fixture(person_fixture):
    post = create_post(person_fixture.id, "content")
    return post


@pytest.fixture()
def posts_fixture(persons_fixture):
    post1 = create_post(persons_fixture[0].id, "content 1")
    post2 = create_post(persons_fixture[1].id, "content 2")
    post3 = create_post(persons_fixture[2].id, "content 3")
    return post1, post2, post3


@pytest.fixture()
def comment_fixture(person_fixture, post_fixture):
    comment = add_comment(post_fixture.id, person_fixture.id, "")
    return comment


@pytest.fixture()
def reply_fixture(comment_fixture, person_fixture):
    reply = reply_to_comment(comment_fixture.id, person_fixture.id, "")
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


@pytest.fixture()
def delete_post(post_fixture):
    return post_fixture


@pytest.fixture()
def post_setup(person_fixture, persons_fixture):
    posted_person_id = person_fixture.id
    content = "post content"
    post = create_post(person_fixture.id, content)
    react_type1 = "haha"
    react_type2 = "wow"
    react_type3 = "like"
    person1 = persons_fixture[0]
    person2 = persons_fixture[1]
    person3 = persons_fixture[2]
    post_react1 = react_to_post(person1, post.id, react_type1)
    post_react2 = react_to_post(person2, post.id, react_type2)
    post_react3 = react_to_post(person3, post.id, react_type3)
    comment_content = "comment content"
    comment1_for_post = add_comment(post.id, person1.id, comment_content)
    comment1_person = person1
    comment1_react1 = react_to_comment(person1, comment1_for_post.id, react_type1)
    comment1_react2 = react_to_comment(person2, comment1_for_post.id, react_type2)
    comment1_react3 = react_to_comment(person3, comment1_for_post.id, react_type3)
    reply1_for_comment1_content = "reply for comment 1"
    reply2_for_comment1_content = "reply2 for comment 1"
    reply1_for_comment1 = reply_to_comment(comment1_for_post.id, person2.id, reply1_for_comment1_content)
    reply1_person = person2
    reply2_for_comment1 = reply_to_comment(comment1_for_post.id, person3.id, reply2_for_comment1_content)
    reply2_person = person3
    react1_for_reply1 = react_to_comment(person3, reply1_for_comment1.id, react_type1)
    react1_for_reply2 = react_to_comment(person2, reply2_for_comment1.id, react_type2)
    return post, person_fixture, post_react1, post_react2, post_react3, person1, person2, person3, comment1_for_post, \
           comment1_person, comment1_react1, comment1_react2, comment1_react3, reply1_for_comment1, \
           reply1_person, reply2_for_comment1, reply2_person, react1_for_reply1, react1_for_reply2, content, \
           comment_content, reply1_for_comment1_content, \
           reply2_for_comment1_content
