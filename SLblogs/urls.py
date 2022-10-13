from django.contrib import admin
from django.urls import path
from appblogs.views import AddPost, ExcluirPost, Home, BlogView, MyBLogs, TodosBlogs, PostView, PublicarView, EditarPost, LikePost, LikeComent, AddBlog

urlpatterns = [
    path('',Home, name = "Home"),
    path('MyBLogs',MyBLogs, name = "MyBLogs"),
    path('AddBlog',AddBlog, name = "AddBlog"),
    path('AddBlog/<str:uid>',AddBlog, name = "AddBlog"),
    path('ExcluirPost/<str:uid>',ExcluirPost, name = "ExcluirPost"),
    path('AddPost/<str:Buid>',AddPost, name = "AddPost"),
    path('AddPost/<str:Buid>/<str:uid>',AddPost, name = "AddPost"),
    path('TodosBlogs',TodosBlogs, name = "TodosBlogs"),
    path('Blog/<str:uid>', BlogView, name = "Blog"),
    path('Post/<str:uid>', PostView, name = "Post"),
    path('LikePost/<str:uid>', LikePost, name = "LikePost"),
    path('LikeComent/<int:id>', LikeComent, name = "LikeComent"),
    path('EditarPost/<str:uid>', EditarPost, name = "EditarPost"),
    path('PublicarView/<str:uid>', PublicarView, name = "PublicarView"),
    path('admin/', admin.site.urls),
]
