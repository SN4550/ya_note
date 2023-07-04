import pytest

from notes.models import Note


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


# Вызываем фикстуру автора и клиента.
@pytest.fixture
def author_client(author, client):
    # Логиним автора в клиенте.
    client.force_login(author)
    return client


@pytest.fixture
def note(author):
    # Создаём объект заметки.
    note = Note.objects.create(
        title='testTitle',
        text='testText',
        slug='testSlug',
        author=author
    )
    return note


@pytest.fixture
def slug_for_args(note):
    return note.slug,


@pytest.fixture
def form_data():
    return {
        'title': 'Заголовок',
        'text': 'Текст',
        'slug': 'slug-slug',
    }
