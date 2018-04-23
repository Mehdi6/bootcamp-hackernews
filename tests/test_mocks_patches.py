from unittest.mock import patch

from django.core.urlresolvers import reverse

from filling_db import create_user
from users.views import UserDetailView


# class UnixFS:
#     @staticmethod
#     def rm(filename):
#         os.remove(filename)
#
#
# def test_unix_fs(mocker):
#     mocker.patch('os.remove')
#     UnixFS.rm('file')
#     os.remove.assert_called_once_with('file')


def test_user_details(client):
    user = create_user()
    with patch.object(UserDetailView, 'get_object', return_value=user):
        url = reverse('users:detail', args=[user.username])
        response = client.get(url)
        print(response)
        assert response.status_code == 200
        assert user.username.encode() in response.content



#
# def test_signup(client):
#     user = create_user()
#     with patch.object(RegisterView, 'get_object', return_value=user):
#         # we test if the user was indeed created
#         response = client.login(username='user', password='password')
#         print(response)
#         assert response == True
#
#
# def test_create_topic(client):
#     user = create_user()
#     topic = create_topic(user)
#     with patch.object(RegisterView, 'get_object', return_value=user):
#         # we test if the user was indeed created
#         response = client.login(username='user', password='password')
#         print(response)
#         assert response == True


# @pytest.mark.django_db(transaction=True)
# def test_create_topic(client):
#     user = create_user()
#     topic = create_topic(user)
#
#     with patch.object(RegisterView, 'form_valid', return_value=user):
#         client.login(username='user', password='password')
#         with patch.object(TopicCreateView, 'post', return_value=topic):
#             url = reverse("services:create_topic")
#             response = client.post(url, {'title': topic.title, 'url': topic.url,
#                               'text': topic.text}, follow=True)
#
#             # we check if the topic was successfully added to the database or not
#             #new_topic = Topic.objects.filter(url=topic.url)
#             assert response.status_code == 200
#             assert topic.title in response.content
#
