from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from services.models import Topic, Comment, UpVoteComment, UpVoteTopic
from users.models import User
from filling_db import create_topic, create_comment, \
                        create_user


class TestTopic(TestCase):
    def setUp(self):
        self.user = create_user()
        self.topic = create_topic(self.user)

    def tearDown(self):
        # tearDown should be called before rolling back the database
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0 and User.objects.count() == 0 and Comment.objects.count() == 0

    def test_create_topic(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse("services:create_topic")

        c.post(url, {'title': self.topic.title, 'url': self.topic.url,
                     'text': self.topic.text}, follow=True)

        # we check if the topic was successfully added to the database or not
        new_topic = Topic.objects.filter(url=self.topic.url)

        assert len(new_topic) == 1

    def test_create_topic_with_missing_required_field(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse("services:create_topic")

        c.post(url, {'url': self.topic.url, 'text': self.topic.text}, follow=True)
        # we check if the topic was not created, given the fact that a
        # required field is missing
        new_topic = Topic.objects.filter(url=self.topic.url)
        assert len(new_topic) == 0

    def test_topic_length(self):
        c = Client()
        c.login(username="user", password='password')
        url = reverse("services:create_topic")
        media = "https://www.thisurlnew.com/"
        title = "c" * 201
        text = "Some text to fill this Topic"

        c.post(url, {'title': title, "media": media, "text": text})

        # check that the comment wasn't added
        comments = Comment.objects.filter(media=media)
        self.assertEqual(len(comments), 0)


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.topic = create_topic(self.user)
        self.topic.save()

    def tearDown(self):
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0 and User.objects.count() == 0 and Comment.objects.count() == 0

    def test_create_comment(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse("services:create_comment", args=[self.topic.id])
        comment = create_comment(self.topic, self.user)
        c.post(url, {'comment_content': comment.content,
                     'comment_media': comment.media}, follow=True)
        # we check if the comment was successfully added to the
        # database or not
        comments = Comment.objects.filter(content=comment.content)

        self.assertEqual(len(comments), 1)
        assert len(comments) == 1

    def test_create_comment_with_missing_required_field(self):
        c = Client()
        c.login(username='user', password='password')
        comment = create_comment(self.topic, self.user)
        url = reverse("services:create_comment", args=[self.topic.id])

        c.post(url, {'comment_media': comment.media})
        # we check if the topic was not created, given the fact that a
        # required field is missing
        comments = Comment.objects.filter(content=comment.content)
        self.assertEqual(len(comments), 0)
        assert len(comments) == 0

    def test_reply_on_comment(self):
        c = Client()
        c.login(username='user', password='password')
        parent_comment = create_comment(self.topic, self.user)
        parent_comment.save()
        url = reverse('services:create_comment',
                      args=[self.topic.id])
        reply_on_comment = Comment(content='reply to comment',
                                   media='https://www.baba.com/',
                                   user=self.user,
                                   topic=self.topic,
                                   parent=parent_comment)

        c.post(url, {'comment_content': reply_on_comment.content,
                     'comment_media': reply_on_comment.media,
                     'comment_parent': reply_on_comment.parent.id})

        # check if the new reply was successfully created
        reply = Comment.objects.filter(media=reply_on_comment.media, parent=reply_on_comment.parent)
        self.assertEqual(len(reply), 1)
        assert len(reply) == 1

    def test_comment_length(self):
        c = Client()
        c.login(username="user", password='password')
        url = reverse("services:create_comment", args=[self.topic.id])
        media = "https://www.thisurlnew.com/"
        content = "c" * 2001
        cmt = Comment(content=content, media=media, topic=self.topic, user=self.user)
        c.post(url, {'content': cmt.content, "media": cmt.media})

        # check that the comment wasn't added
        result = Comment.objects.filter(media=media)

        self.assertEqual(len(result), 0)
        assert len(result) == 0


class UpvoteTopicTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.topic = create_topic(self.user)
        self.topic.save()

    def tearDown(self):
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0 and User.objects.count() == 0 and Comment.objects.count() == 0

    def test_upvote_topic(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse('services:topic_upvote')
        c.post(url, data={'id': self.topic.id})

        # check if the topic was upvoted
        upvote = UpVoteTopic.objects.filter(topic=self.topic, user=self.user)
        self.assertEqual(len(upvote), 1)
        assert len(upvote) == 1

    def test_upvote_upvoted_topic(self):
        c = Client()
        c.login(username=self.user, password='password')

        up = UpVoteTopic(user=self.user, topic=self.topic)
        up.save()

        # We check if the topic will be upvoted after being upvoted
        # It should not be possible!
        url = reverse('services:topic_upvote')
        result = c.post(url, data={'id': self.topic.id})

        self.assertEqual(result.status_code, 400)
        assert result.status_code == 400


class UpvoteCommentTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.topic = create_topic(self.user)
        self.topic.save()
        self.comment = create_comment(self.topic, self.user)
        self.comment.save()

    def tearDown(self):
        Comment.objects.all().delete()
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0 and User.objects.count() == 0 and Comment.objects.count() == 0

    def test_upvote_comment(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse('services:comment_upvote')
        c.post(url, data={'id': self.comment.id})

        # check if the topic was upvoted
        upvote = UpVoteComment.objects.filter(comment=self.comment, user=self.user)
        self.assertEqual(len(upvote), 1)
        assert len(upvote) == 1

    def test_upvote_upvoted_comment(self):
        c = Client()
        c.login(username='user', password='password')
        url = reverse('services:comment_upvote')
        up = UpVoteComment(user=self.user, comment=self.comment)
        up.save()
        # We check if the comment will be upvoted after being upvoted
        # It should not be possible!
        result = c.post(url, data={'id': self.comment.id})

        self.assertEqual(result.status_code, 400)
        assert result.status_code == 400
