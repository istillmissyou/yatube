from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_names(self):
        expected_object_name = self.group.title
        self.assertEqual(expected_object_name, str(self.group))

        expected_object_name = self.post.text
        self.assertEqual(expected_object_name, str(self.post))
