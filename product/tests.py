from django.test import TestCase
import random
import string
from django.contrib.auth.models import User
from product.models import Profile, Comments, Item



class test_profiles(TestCase):
    def setUp(self):
        length = random.randint(1,20)
        random_sequence = ''.join(random.choice(string.printable) for i in range(length))
        self.test_user = User.objects.create_user(
            username=random_sequence,
            password=random_sequence,
        )

    def test_users(self):
        self.assertEqual(self.test_user.is_active, True)
        self.assertEqual(self.test_user.is_anonymous, False)
        self.assertEqual(self.test_user.is_staff, False)
        self.assertEqual(self.test_user.is_superuser, False)

    def test_login(self):
        length = random.randint(1,20)
        random_sequence = ''.join(random.choice(string.printable) for i in range(length))
        self.test_user = User.objects.create_user(
            username=random_sequence,
            password=random_sequence,
        )
        self.test_user.set_password(random_sequence)
        self.test_user.save()
        response = self.client.login(username = random_sequence, password = random_sequence)
        self.assertEqual(response, True)

