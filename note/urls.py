from django.contrib import admin
from django.urls import path,include
from note.views import NoteCreateList,NoteRetriveUpdateDestroy

urlpatterns = [
    path('', NoteCreateList.as_view() , name='notes'),
    path('<str:pk>', NoteRetriveUpdateDestroy.as_view() , name='note')
]

