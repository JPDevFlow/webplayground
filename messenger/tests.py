from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message 

# Create your tests here.

class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None,'test1234')
        self.user2 = User.objects.create_user('user2', None,'test1234')
        
        self.thread = Thread.objects.create()

    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()), 2)