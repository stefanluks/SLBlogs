from email.policy import default
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    UID = models.CharField("Código UID do Blog", max_length=150, null =True, blank = True)
    nome = models.CharField("Nome do Blog", max_length=150)
    descricao = models.TextField("Descrição do blog", max_length=1500, null=True, blank=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.CharField("Tema do BLOG", max_length=50, null=True, blank=True)
    posts = models.ManyToManyField("Post",related_name="lista_posts", blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.UID = self.nome.replace(" ", "-").replace("ã","a").replace("é","e").replace("à","a").replace("ô","o")
        super().save(*args, **kwargs)

    def GetQtdPosts(self):
        return len(list(self.posts.all()))

    def GetQtdLikes(self):
        cont = 0
        for p in self.posts.all():
            cont += p.GetQtdLikes()
        return cont

    def GetQtdComents(self):
        cont = 0
        for p in self.posts.all():
            cont += p.GetQtdComents()
        return cont


class Post(models.Model):
    UID = models.CharField("Código UID do POST", max_length=150, null=True, blank=True)
    titulo = models.CharField("Titulo do POST", max_length=150)
    tema = models.CharField("Tema do POST", max_length=50, null=True, blank=True)
    resumo = models.TextField("Resumo do post", max_length=2000, null=True, blank=True)
    publicado = models.BooleanField("Está publicado?", default=False)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, related_name="Blog_relacionado", null=True, blank=True)
    conteudo = models.TextField("Conteudo do post [ HTML ]", max_length=50000, null = True, blank = True)

    def __str__(self):
        return self.titulo

    def GetQtdLikes(self):
        return len(list(Like.objects.filter(post = self)))

    def GetComentarios(self):
        saida = []
        lista = list(Comentario.objects.filter(post=self))
        for c in lista:
            if not c.e_resposta:
                saida.append(c)
        return saida

    def GetQtdComents(self):
        return len(self.GetComentarios())
        
    def save(self, *args, **kwargs):
        self.UID = self.titulo.replace(" ", "-").replace("ã","a").replace("é","e").replace("à","a").replace("ô","o")
        super().save(*args, **kwargs)


class Like(models.Model):
    post = models.ForeignKey(Post,related_name = "Post_Like", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,related_name = "Usuario_like", on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username + " Curtiu o post: "+ self.post.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, related_name="Post_coment", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name="Usuario_coment", on_delete=models.CASCADE)
    conteudo = models.TextField("Conteúdo do comentario", max_length=500)
    e_resposta = models.BooleanField("É uma resposta", default=False)
    
    def __str__(self):
        return self.usuario.username + " comentou no post ID ["+str(self.pk)+"]:"+ self.post.titulo
    
    def CheckLike(self, usuario):
        for lc in LikeComentario.objects.filter(comentario = self):
            if lc.usuario == usuario:
                return True
        return False

    def GetQtdLikes(self):
        return len(list(LikeComentario.objects.filter(comentario = self)))
    
    def GetQtdComents(self):
        return len(self.GetRespostas())

    def GetRespostas(self):
        return list(Resposta.objects.filter(comentario = self))


class Resposta(Comentario):
    comentario = models.ForeignKey(Comentario,related_name = "Comentario_Resposta", on_delete=models.CASCADE)


class LikeComentario(models.Model):
    comentario = models.ForeignKey(Comentario,related_name = "Comentario", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,related_name = "Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username + " curitur o comentário: [ "+ str(self.comentario.id)+" ]"