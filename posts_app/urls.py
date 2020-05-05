from django.urls import path
from . import views

urlpatterns = [
    path('posts/p/<int:page>', views.posts, name="posts_page"),
    path('posts/<int:post_id>', views.post, name="post"),
    path('', views.posts, name="posts"),

    #todo change hashtags and date to path param
]
