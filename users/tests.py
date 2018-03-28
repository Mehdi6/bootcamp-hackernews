from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import User


def create_superuser():
    super_user = User(
        username='admin',
        email='admin@email.com',
        full_name='testing user',
        is_active=True,
        is_staff=True,
        profile_picture='https://www.wallstreetotc.com/wp-content/uploads/2014/10/facebook-anonymous-app.jpg',
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
        profile_picture='https://www.wallstreetotc.com/wp-content/uploads/2014/10/facebook-anonymous-app.jpg',
    )

    new_user.set_password("password")
    new_user.save()
    return new_user


# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.url = reverse("user:user_profile")

    def doCleanups(self):
        self.new_user.delete()
        self.superuser.delete()