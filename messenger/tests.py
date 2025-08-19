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

    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    def test_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)
