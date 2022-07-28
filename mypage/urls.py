from django.urls import path, re_path
from . import views
from .views import *
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

app_name = "mypage"
urlpatterns = [
    path('mypage/<int:id>', views.mypage, name='mypage'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()),
         name='profile_update'),
    path('<int:id>/follow', views.follow, name="follow"),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
