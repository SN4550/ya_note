from django.urls import path

from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # +
    # добавляем запись
    path('add/', views.NoteCreate.as_view(), name='add'),    # +
    # редактируем запись
    path('edit/<slug:slug>/', views.NoteUpdate.as_view(), name='edit'),
    # страница записи
    path('note/<slug:slug>/', views.NoteDetail.as_view(), name='detail'),
    # удаление записи
    path('delete/<slug:slug>/', views.NoteDelete.as_view(), name='delete'),
    # список всех записей
    path('notes/', views.NotesList.as_view(), name='list'),
    # редирект после успешной записи
    path('done/', views.NoteSuccess.as_view(), name='success'),
]
