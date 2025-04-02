from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>", views.syllabus, name="syllabus"),
    path("<int:year>/<str:code>", views.syllabus, name="syllabus"),
    path("chat", views.chat, name="chat"),
]