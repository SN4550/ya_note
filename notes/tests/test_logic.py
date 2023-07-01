from notes.models import Note


def test_adding_note(self):
    note_count = Note.objects.count()
    self.assertEqual(note_count, 1)
