import pytest
from django.urls import reverse


# В тесте используем фикстуру заметки
# и фикстуру клиента с автором заметки.
def test_note_in_list_for_author(note, author_client):
    url = reverse('notes:list')
    # Запрашиваем страницу со списком заметок:
    response = author_client.get(url)
    # Получаем список объектов из контекста:
    object_list = response.context['object_list']
    # Проверяем, что заметка находится в этом списке:
    assert note in object_list


# В этом тесте тоже используем фикстуру заметки,
# но в качестве клиента используем admin_client;
# он не автор заметки, так что заметка не должна быть ему видна.
def test_note_not_in_list_for_another_user(note, admin_client):
    url = reverse('notes:list')
    response = admin_client.get(url)
    object_list = response.context['object_list']
    assert note not in object_list


@pytest.mark.parametrize(
    # Задаём названия для параметров:
    ['parametrized_client', 'note_in_list'],
    [
            # Передаём фикстуры в параметры при помощи "ленивых фикстур":
            (pytest.lazy_fixture('author_client'), True),
            (pytest.lazy_fixture('admin_client'), False),
    ]
)
def test_notes_list_for_different_users(
        parametrized_client, note, note_in_list):
    url = reverse('notes:list')
    # Выполняем запрос от имени параметризованного клиента:
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    # Проверяем истинность утверждения "заметка есть в списке"
    assert (note in object_list) is note_in_list


@pytest.mark.parametrize(
    ['name', 'args'],
    [
        ('notes:add', None),
        ('notes:edit', pytest.lazy_fixture('slug_for_args'))
    ]
)
def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
