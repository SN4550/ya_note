from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutesAppNotes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auth_user = User.objects.create(username='authUser')
        cls.anonymous = User.objects.create(username='anonymousUser')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Содержание',
            slug='test_slug',
            author=cls.auth_user)

    def test_redirect_for_anonymous_user(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
            ('notes:success', None)
        )
        for path, args in urls:
            with self.subTest(path=path):
                url = reverse(path, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)


class TestRoutesProjectYaNote(TestCase):
    def test_availability_of_auth_paths(self):
        urls_paths = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None))
        for path in urls_paths:
            path_name, args = path
            with self.subTest(
                    path_name=path_name, msg=f'ULR {path_name} не существует'):
                url = reverse(path_name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
