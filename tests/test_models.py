from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from services.models import Topic, Comment, UpVoteComment, UpVoteTopic
from users.models import User
from filling_db import generate_dump_data, create_topic, create_comment


class TestTopic(TestCase):
    def setUp(self):
        """setUp should be called after starting a transaction"""
        # assert Topic.objects.count() == 0
        generate_dump_data()
        self.users = User.objects.all()

    def test_create_topic(self):
        c = Client()
        c.login(username='user0', password='password0')
        url = reverse("services:create_topic")
        topic = create_topic(self.users[0])
        results = c.post(url, {'title': topic.title, 'url': topic.url,
                     'text': topic.text})
        print(results.status_code)
        # we check if the topic was successfully added to the database or not
        new_topic = Topic.objects.filter(url=topic.url)
        self.assertEqual(len(new_topic), 1)
    
    def test_create_topic_with_missing_required_field(self):
        c = Client()
        topic = create_topic(self.users[0])
        auth = c.login(username='user0', password='password0')
        url = reverse("services:create_topic")

        c.post(url, {'url': topic.url, 'text': topic.text})
        # we check if the topic was not created, given the fact that a
        # required field is missing
        new_topic = Topic.objects.filter(url=topic.url)

        self.assertEqual(len(new_topic), 0)

    def test_topic_length(self):
        c = Client()
        c.login(username="user0", password='password0')
        url = reverse("services:create_topic")
        media = "https://www.thisurlnew.com/"
        title = "c" * 201
        text = "Some text to fill this Topic"

        c.post(url, {'title': title, "media": media, "text": text})

        # check that the comment wasn't added
        comments = Comment.objects.filter(media=media)
        self.assertEqual(len(comments), 0)

    def tearDown(self):
        # tearDown should be called before rolling back the database
        UpVoteTopic.objects.all().delete()
        UpVoteComment.objects.all().delete()
        Comment.objects.all().delete()
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0


class CommentTestCase(TestCase):
    def setUp(self):
        generate_dump_data()
        self.users = User.objects.all()
        self.topic = create_topic(self.users[0])
        self.topic.save()

    def tearDown(self):
        UpVoteTopic.objects.all().delete()
        UpVoteComment.objects.all().delete()
        Comment.objects.all().delete()
        Topic.objects.all().delete()
        User.objects.all().delete()

        assert Topic.objects.count() == 0 and User.objects.count()==0 and Comment.objects.count()==0

    def test_create_comment(self):
        c = Client()
        c.login(username='user0', password='password0')
        url = reverse("services:create_comment", args=[self.topic.id])
        comment = create_comment(self.topic, self.users[0])
        c.post(url, {'comment_content': comment.content,
                     'comment_media': comment.media})
        # we check if the topic was successfully added to the
        # database or not
        comments = Comment.objects.filter(content=comment.content)
        self.assertEqual(len(comments), 1)

    def test_create_comment_with_missing_required_field(self):
        c = Client()
        c.login(username='user0', password='password0')
        comment = create_comment(self.topic, self.users[0])
        url = reverse("services:create_comment", args=[self.topic.id])

        c.post(url, {'comment_media': comment.media})
        # we check if the topic was not created, given the fact that a
        # required field is missing
        comments = Comment.objects.filter(content=comment.content)
        self.assertEqual(len(comments), 0)

    def test_reply_on_comment(self):
        c = Client()
        c.login(username='user0', password='password0')
        parent_comment = create_comment(self.topic, self.users[0])
        parent_comment.save()
        url = reverse('services:create_comment',
                      args=[self.topic.id])
        reply_on_comment = Comment(content='reply to comment',
                                   media='https://www.baba.com/',
                                   user=self.users[0],
                                   topic=self.topic,
                                   parent=parent_comment)

        c.post(url, {'comment_content': reply_on_comment.content,
                     'comment_media': reply_on_comment.media,
                     'comment_parent': reply_on_comment.parent.id})

        # check if the new reply was successfully created
        reply = Comment.objects.filter(media=reply_on_comment.media, parent=reply_on_comment.parent)
        self.assertEqual(len(reply), 1)

    def test_comment_length(self):
        c = Client()
        c.login(username="user0", password='password0')
        url = reverse("services:create_comment", args=[self.topic.id])
        media = "https://www.thisurlnew.com/"
        content = "c"*2001
        cmt = Comment(content=content, media=media, topic=self.topic, user=self.users[0])
        c.post(url, {'content': cmt.content, "media": cmt.media})

        # check that the comment wasn't added
        result = Comment.objects.filter(media=media)

        self.assertEqual(len(result), 0)
