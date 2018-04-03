from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from users.models import User
from .models import (Topic, Comment, UpVoteTopic, UpVoteComment)


def create_superuser():
    super_user = User(
        username='admin',
        email='admin@email.com',
        full_name='testing user',
        is_active=True,
        is_staff=True,
        profile_picture='https://www.wallstreetotc.com/wp-content/\
        uploads/2014/10/facebook-anonymous-app.jpg',
    )

    super_user.set_password("admin")
    super_user.save()
    return super_user


def create_user():
    new_user = User(
        username='user',
        email='user@email.com',
        full_name='testing user',
        is_active=True,
        is_staff=False,
        profile_picture='https://www.wallstreetotc.com/wp-content/uplo\
        ads/2014/10/facebook-anonymous-app.jpg',
    )

    new_user.set_password("password")
    new_user.save()
    return new_user


def create_topic(user):
    return Topic(title="This is a test title, for our awesome \
                testing topic", url="http://www.someurltotest.com/",
                 text="blablabla", user=user)


class TopicTestCase(TestCase):

    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.topic = create_topic(self.new_user)

    def doCleanups(self):
        self.new_user.delete()
        self.superuser.delete()

    def test_create_topic(self):
        c = Client()
        auth = c.login(username='user', password='password')
        url = reverse("services:create_topic")
        topic = create_topic(self.new_user)
        c.post(url, {'title': topic.title, 'url': topic.url,
                     'text': topic.text})
        # we check if the topic was successfully added to the database or not
        new_topic = Topic.objects.filter(url=topic.url)
        self.assertEqual(len(new_topic), 1)

    def test_create_topic_with_missing_required_field(self):
        c = Client()
        auth = c.login(username='user', password='password')
        url = reverse("services:create_topic")

        c.post(url, {'url': self.topic.url, 'text': self.topic.text})
        # we check if the topic was not created, given the fact that a
        # required field is missing
        new_topic = Topic.objects.filter(url=self.topic.url)
        self.assertEqual(len(new_topic), 0)


def create_comment(topic, user):
    return Comment(content='The testing comment content',
                   media='https://www.someurlfortest.com/',
                   topic=topic, user=user)


class CommentTestCase(TestCase):
    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.topic = create_topic(self.new_user)
        self.topic.save()

    def doCleanups(self):
        self.new_user.delete()
        self.superuser.delete()
        self.topic.delete()

    def test_create_comment(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse("services:create_comment", args=[self.topic.id])
        comment = create_comment(self.topic, self.new_user)
        c.post(url, {'comment_content': comment.content,
                     'comment_media': comment.media})
        # we check if the topic was successfully added to the
        # database or not
        comments = Comment.objects.filter(content=comment.content)
        self.assertEqual(len(comments), 1)

    def test_create_comment_with_missing_required_field(self):
        c = Client()
        c.login(username='user', password='password')
        comment = create_comment(self.topic, self.new_user)
        url = reverse("services:create_comment", args=[self.topic.id])

        c.post(url, {'comment_media': comment.media})
        # we check if the topic was not created, given the fact that a
        # required field is missing
        comments = Comment.objects.filter(content=comment.content)
        self.assertEqual(len(comments), 0)

    def test_reply_on_comment(self):
        c = Client()
        c.login(username='user', password='password')
        parent_comment = create_comment(self.topic, self.new_user)
        parent_comment.save()
        url = reverse('services:create_comment',
                      args=[self.topic.id])
        reply_on_comment = Comment(content='reply to comment',
                                   media='https://www.baba.com/',
                                   user=self.superuser,
                                   topic=self.topic,
                                   parent=parent_comment)

        c.post(url, {'comment_content': reply_on_comment.content,
                     'comment_media': reply_on_comment.media,
                     'comment_parent': reply_on_comment.parent.id})

        # check if the new reply was successfully created
        reply = Comment.objects.filter(media=reply_on_comment.media, parent=reply_on_comment.parent)
        self.assertEqual(len(reply), 1)


class UpvoteTopicTestCase(TestCase):
    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.topic = create_topic(self.new_user)
        self.topic.save()

    def doCleanups(self):
        self.new_user.delete()
        self.superuser.delete()
        self.topic.delete()

    def test_upvote_topic(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse('services:topic_upvote', args=[self.topic.id])
        c.post(url)

        # check if the topic was upvoted
        upvote = UpVoteTopic.objects.filter(topic=self.topic, user=self.new_user)
        self.assertEqual(len(upvote), 1)


class UpvoteCommentTestCase(TestCase):
    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.topic = create_topic(self.superuser)
        self.topic.save()
        self.comment = create_comment(self.topic, self.new_user)
        self.comment.save()

    def doCleanups(self):
        self.new_user.delete()
        self.superuser.delete()
        self.topic.delete()
        self.comment.delete()

    def test_upvote_comment(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse('services:comment_upvote', args=[self.comment.id])
        c.post(url)

        # check if the topic was upvoted
        upvote = UpVoteComment.objects.filter(comment=self.comment, user=self.new_user)
        self.assertEqual(len(upvote), 1)

