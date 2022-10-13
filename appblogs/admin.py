from django.contrib import admin
from .models import Blog, Like, Comentario, LikeComentario, Resposta, Post

admin.site.register(Blog)
admin.site.register(Like)
admin.site.register(Comentario)
admin.site.register(LikeComentario)
admin.site.register(Resposta)
admin.site.register(Post)
