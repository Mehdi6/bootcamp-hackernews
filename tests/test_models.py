import pytest
from django.core.urlresolvers import reverse
from unittest.mock import patch

from services.models import Topic, Comment, UpVoteComment, UpVoteTopic
from filling_db import create_topic, create_comment, \
    create_user


@pytest.mark.django_db(transaction=True)
def test_user_signup(client):
    user = create_user()

    with patch('allauth.account.utils.send_email_confirmation'):
        url = reverse('signup')
        password = 'somepassword'
        response = client.post(url, {'username': user.username, 'email': user.email,
                               'full_name': user.full_name, 'password1':password, 'password2': password},
                               follow=True)

        assert response.status_code == 200
        assert 'One-Time password sent'.encode() in response.content


@pytest.mark.django_db(transaction=True)
def test_create_topic(client):
    user = create_user(save=True)
    topic = create_topic(user)
    client.login(username='user', password='password')
    url = reverse("services:create_topic")

    client.post(url, {'title': topic.title, 'url': topic.url,
                      'text': topic.text}, follow=True)

    # we check if the topic was successfully added to the database or not
    new_topic = Topic.objects.filter(url=topic.url)

    assert len(new_topic) == 1


@pytest.mark.django_db(transaction=True)
def test_create_topic_with_missing_required_field(client):
    user = create_user(save=True)
    topic = create_topic(user)
    client.login(username='user', password='password')
    url = reverse("services:create_topic")

    client.post(url, {'url': topic.url, 'text': topic.text}, follow=True)
    # we check if the topic was not created, given the fact that a
    # required field is missing
    new_topic = Topic.objects.filter(url=topic.url)
    assert len(new_topic) == 0


@pytest.mark.django_db(transaction=True)
def test_topic_length(client):
    client.login(username="user", password='password')
    url = reverse("services:create_topic")
    media = "https://www.thisurlnew.com/"
    title = "c" * 201
    text = "Some text to fill this Topic"

    client.post(url, {'title': title, "media": media, "text": text})

    # check that the comment wasn't added
    comments = Comment.objects.filter(media=media)
    assert len(comments) == 0


@pytest.mark.django_db(transaction=True)
def test_create_comment(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    url = reverse("services:create_comment", args=[topic.id])
    comment = create_comment(topic, user)
    client.post(url, {'comment_content': comment.content,
                      'comment_media': comment.media}, follow=True)
    # we check if the comment was successfully added to the
    # database or not
    comments = Comment.objects.filter(content=comment.content)

    # assertEqual(len(comments), 1)
    assert len(comments) == 1


@pytest.mark.django_db(transaction=True)
def test_create_comment_with_missing_required_field(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    comment = create_comment(topic, user)
    url = reverse("services:create_comment", args=[topic.id])

    client.post(url, {'comment_media': comment.media})
    # we check if the topic was not created, given the fact that a
    # required field is missing
    comments = Comment.objects.filter(content=comment.content)
    # assertEqual(len(comments), 0)
    assert len(comments) == 0


@pytest.mark.django_db(transaction=True)
def test_reply_on_comment(client, django_db_setup):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    parent_comment = create_comment(topic, user, save=True)
    url = reverse('services:create_comment',
                  args=[topic.id])
    reply_on_comment = Comment(content='reply to comment',
                               media='https://www.baba.com/',
                               user=user,
                               topic=topic,
                               parent=parent_comment)

    client.post(url, {'comment_content': reply_on_comment.content,
                      'comment_media': reply_on_comment.media,
                      'comment_parent': reply_on_comment.parent.id})

    # check if the new reply was successfully created
    reply = Comment.objects.filter(media=reply_on_comment.media, parent=reply_on_comment.parent)
    # assertEqual(len(reply), 1)
    assert len(reply) == 1


@pytest.mark.django_db(transaction=True)
def test_comment_length(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username="user", password='password')
    url = reverse("services:create_comment", args=[topic.id])
    media = "https://www.thisurlnew.com/"
    content = "c" * 2001
    cmt = Comment(content=content, media=media, topic=topic, user=user)
    client.post(url, {'content': cmt.content, "media": cmt.media})

    # check that the comment wasn't added
    result = Comment.objects.filter(media=media)

    # assertEqual(len(result), 0)
    assert len(result) == 0


@pytest.mark.django_db(transaction=True)
def test_upvote_topic(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    url = reverse('services:topic_upvote')
    client.post(url, data={'id': topic.id})

    # check if the topic was upvoted
    upvote = UpVoteTopic.objects.filter(topic=topic, user=user)
    # assertEqual(len(upvote), 1)
    assert len(upvote) == 1


@pytest.mark.django_db(transaction=True)
def test_upvote_upvoted_topic(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username=user, password='password')

    up = UpVoteTopic(user=user, topic=topic)
    up.save()

    # We check if the topic will be upvoted after being upvoted
    # It should not be possible!
    url = reverse('services:topic_upvote')
    result = client.post(url, data={'id': topic.id})

    # assertEqual(result.status_code, 400)
    assert result.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_upvote_comment(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    comment = create_comment(topic, user, save=True)
    url = reverse('services:comment_upvote')
    client.post(url, data={'id': comment.id})

    # check if the topic was upvoted
    upvote = UpVoteComment.objects.filter(comment=comment, user=user)
    # assertEqual(len(upvote), 1)
    assert len(upvote) == 1


@pytest.mark.django_db(transaction=True)
def test_upvote_upvoted_comment(client):
    user = create_user(save=True)
    topic = create_topic(user, save=True)
    client.login(username='user', password='password')
    comment = create_comment(topic, user, save=True)
    url = reverse('services:comment_upvote')
    up = UpVoteComment(user=user, comment=comment)
    up.save()
    # We check if the comment will be upvoted after being upvoted
    # It should not be possible!
    result = client.post(url, data={'id': comment.id})

    # assertEqual(result.status_code, 400)
    assert result.status_code == 400
