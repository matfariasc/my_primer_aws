from django.urls import path
from . import views

urlpatterns = [
    path('wall/', views.wall_index, name="index_wall"),
    path('', views.index_login, name="index_login"),
    path('register/new_user', views.new_user, name="new_user" ),
    path('user/log_out', views.log_out, name="log_out"),
    path('user/login', views.login, name="login"),
    path('post/new', views.post_new, name="post_new"),
    path('comment/new', views.comment_new, name="comment_new")
]
