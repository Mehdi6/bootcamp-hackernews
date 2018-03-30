import string
import random
from services.models import Topic, Comment, UpVoteTopic
from users.models import User
from django.test import Client

c = Client()
c.login(username='user', password='password')


# creating a user first
def create_user():
    users = User.objects.filter(username='user')
    if len(users) == 1:
        return users[0]

    new_user = User(
        username='user',
        email='user@email.com',
        full_name='testing user',
        is_active=True,
        is_staff=False,
        profile_picture='https://www.wallstreetotc.com/wp-content/\
        uploads/2014/10/facebook-anonymous-app.jpg',
    )

    new_user.set_password("password")
    new_user.save()
    return new_user


def string_generator(size=6, chars=string.ascii_lowercase +
                                   string.digits + '    '):
    return ''.join(random.choice(chars) for _ in range(size))


def create_topic(user):
    random_title = string_generator(size=100)
    random_text = string_generator(size=300)
    random_url = "https://" + string_generator(size=20) + ".com/"

    topic = Topic(title=random_title,
                  text=random_text,
                  url=random_url,
                  user=user
                  )

    return topic


def create_comment(topic, user):
    content = string_generator(size=300)
    media = "https://" + string_generator(size=20) + ".com/"

    comment = Comment(content=content,
                      media=media,
                      user=user,
                      topic=topic,
                      )

    return comment


def create_reply(comment, user):
    content = string_generator(size=300)
    media = "https://" + string_generator(size=20) + ".com/"

    reply = Comment(content=content,
                    media=media,
                    user=user,
                    topic=comment.topic,
                    parent=comment,
                    )

    return reply


def generate_dump_data():
    user = create_user()

    for _ in range(100):
        topic = create_topic(user=user)
        topic.save()

        upvote_topic(topic)
        # two comments on each topic
        for _ in range(2):
            comment = create_comment(topic, user)
            comment.save()
            # two replies on each comment
            for _ in range(2):
                reply = create_reply(comment, user)
                reply.save()


def upvote_topic(topic):
    users = User.objects.all()
    users_number = len(users)
    i = random.randint(0, users_number)

    for j in range(i):
        up = UpVoteTopic(user=users[j], topic=topic)
        up.save()


generate_dump_data()
