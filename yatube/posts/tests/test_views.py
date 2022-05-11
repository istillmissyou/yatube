from linecache import cache
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post

User = get_user_model()

COUNT_SECOND_PAGE = 3


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Danil')
        cls.user2 = User.objects.create_user(username='Polina')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}):
            'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_show_correct_context(self):
        templates_pages_names = (
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user.username})
        )
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                post_object = response.context['page_obj'][0]
                self.assertEqual(post_object.id, self.post.id)
                self.assertEqual(post_object.text, self.post.text)
                self.assertEqual(post_object.author, self.post.author)
                self.assertEqual(post_object.group, self.post.group)
                self.assertEqual(post_object.image, self.post.image)

    def test_post_detail_page_show_correct_context(self):
        reverse_name = reverse('posts:post_detail',
                               kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(reverse_name)
        self.assertEqual(response.context['post'].id, self.post.id)
        self.assertEqual(response.context['post'].text, self.post.text)
        self.assertEqual(response.context['post'].image, self.post.image)

    def test_create_form_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_cache_index_page(self):
        response = self.client.get(reverse('posts:index'))
        Post.objects.all().delete()
        self.assertTrue(self.post.text.encode() in response.content)
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        self.assertFalse(self.post.text.encode() in response.content)

    def test_follow_and_unfollow_author(self):
        follow_count = Follow.objects.count()
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user2.username}
            )
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(Follow.objects.filter(user=self.user,
                                              author=self.user2).exists())
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user2.username}
            )
        )
        self.assertEqual(Follow.objects.count(), 0)
        self.assertFalse(Follow.objects.filter(user=self.user,
                                               author=self.user2).exists())


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Danil')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        for i in range(13):
            cls.post = Post.objects.create(
                text=f'Напишем текст {i}',
                author=cls.user,
                group=cls.group
            )

        cls.template_pages = (
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.post.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.post.author})
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        for template_page in self.template_pages:
            with self.subTest(template_page):
                response = self.authorized_client.get(template_page)
                self.assertEqual(len(response.context['page_obj']),
                                 settings.COUNTOBJ)

    def test_second_page_contains_three_records(self):
        for template_page in self.template_pages:
            with self.subTest(template_page):
                response = self.authorized_client.get((template_page)
                                                      + '?page=2')
                self.assertEqual(len(response.context['page_obj']),
                                 COUNT_SECOND_PAGE)
