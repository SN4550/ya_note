from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestNotesList(TestCase):
    LIST_PAGE = reverse('notes:list')
    COUNT_NOTE = 10

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        Note.objects.bulk_create(
            Note(
                title=f'Заголовок {i}',
                text=f'Содержание {i}',
                slug=f'testSlug_{i}',
                author=cls.author)
            for i in range(cls.COUNT_NOTE))

    def test_the_number_of_records_per_page(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_PAGE)
        object_list = response.context['object_list']
        count_note = len(object_list)
        self.assertEqual(count_note, self.COUNT_NOTE)


class TestDetailNotePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.user = User.objects.create(username='Аноним')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Содержание',
            slug='test_Slug',
            author=cls.author)
        cls.detail_url = reverse('notes:edit', args=(cls.note.slug,))

    def test_anonymous_user_access_to_the_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_auth_user_access_to_the_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)

