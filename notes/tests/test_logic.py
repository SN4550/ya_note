from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestNoteCreations(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testAuthor')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.url = reverse('notes:success', None)
        cls.form_data = {
            'title': 'testTitle',
            'text': 'text in form'}

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, 'title in form')
        self.assertEqual(note.slug, 'formSlug')
        self.assertEqual(note.author, self.author)

    def test_user_cant_use_not_unique_slug(self):
        self.note = Note.objects.create(
            title='testTitle',
            text='testText',
            author=self.author)
        response = self.auth_client.post(self.url, data=self.form_data)
        """ ИСПОЛЬЗОВАТЬ ДРУГИЕ URL """
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=WARNING)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)


class TestEditDeleteNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.author = User.objects.create(username='testAuthor')
        cls.note = Note.objects.create(
            title='testTitle',
            text='testText',
            slug='testSlug',
            author=cls.author)

    def test_author_can_delete_note(self):
        ...

    def test_user_cant_delete_note_of_another_user(self):
        ...

    def test_author_can_edit_note(self):
        ...

    def test_user_cant_edit_note_of_another_user(self):
        ...



