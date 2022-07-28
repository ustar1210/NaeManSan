from django.urls import path
from main import views
from .views import *

app_name = "main"
urlpatterns = [
    path('', showmain, name="showmain"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('pricing/', pricing, name="pricing"),
    path('work-single/', worksingle, name="worksingle"),
    path('work/', work, name="work"),
    path('studying/', studying, name="studying"),
    path('plan/', plan, name="plan"),
    path('<str:id>', plan_detail, name="plan_detail"),
    path('plan_new/', plan_new, name="plan_new"),
    path('plan_create/', plan_create, name="plan_create"),
    path('plan_edit/<str:id>', plan_edit, name="plan_edit"),
    path('plan_update/<str:id>', plan_update, name="plan_update"),
    path('plan_delete/<str:id>', plan_delete, name="plan_delete"),
    path('<str:plan_id>/create_comment',create_comment,name='create_comment'),
    path('<str:comment_id>/edit_comment',edit_comment,name='edit_comment'),
    path('<str:comment_id>/update_comment',update_comment,name='update_comment'),
    path('<str:comment_id>/delete_comment',delete_comment,name='delete_comment'),
    path('diary_detail/<int:id>',diary_detail, name='diary_detail'),
    path('diary_new/', diary_new, name='diary_new'),
    path('diary_create/', diary_create, name="diary_create"),
    path('studydate_create/', studydate_create, name="studydate_create"),
]
