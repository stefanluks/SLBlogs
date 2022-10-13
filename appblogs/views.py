from django.shortcuts import render, redirect
from .models import Blog, Comentario, LikeComentario, Post, Like
from .forms import FormBlog, FormPost

def GetPostsMaisCurtidos():
    temp = list(Post.objects.all())
    lista = []
    maximo = 10
    if len(temp) < maximo:
        maximo = len(temp)
    for i in range(maximo):
        maisLike = 0
        maior = None
        pos = 0
        for p in range(len(temp)):
            if temp[p].GetQtdLikes() > maisLike:
                maisLike = temp[p].GetQtdLikes()
                maior = temp[p]
                pos = p
        lista.append(maior)
        temp.pop(pos)
    return lista


def Home(request):
    return render(request, 'home.html', {
        "blogs":Blog.objects.all()[:3],
        "posts":GetPostsMaisCurtidos()
    })


def MyBLogs(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(dono = request.user)
    return render(request, 'myBlogs.html', {
        "blogs": blogs
    })


def AddBlog(request, uid = None):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = FormBlog()
            if uid and Blog.objects.filter(UID = uid):
                blog = Blog.objects.get(UID = uid)
                form = FormBlog(instance=blog)
            return render(request, 'addBlog.html', {
                "title":"Novo Blog",
                "form":form,
                "UID":uid
            })
        elif request.method == "POST":
            blog = Blog()
            if uid and Blog.objects.filter(UID = uid):
                blog = Blog.objects.get(UID = uid)
            blog.nome = request.POST["nome"]
            blog.descricao = request.POST["descricao"]
            blog.tema = request.POST["tema"]
            blog.dono = request.user
            blog.save()
            return redirect("Blog",blog.UID)
    else:
        return render(request, 'erro.html', {
            "msg":"Crie um conta antes de criar um blog!",
        })


def AddPost(request,Buid, uid = None):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = FormPost()
            post = blog = None
            edicao = False
            if Blog.objects.filter(UID = Buid):
                blog = Blog.objects.get(UID = Buid)
            if uid and Post.objects.filter(UID = uid):
                edicao = True
                post = Post.objects.get(UID = uid)
                form = FormPost(instance=post)
            return render(request, 'addPost.html', {
                "title":"Novo Post",
                "form":form,
                "edicao":edicao,
                "post":post,
                "UID":uid,
                "blog": blog
            })
        elif request.method == "POST":
            post = Post()
            blog = None
            if Blog.objects.filter(UID = Buid):
                blog = Blog.objects.get(UID = Buid)
            if uid and Post.objects.filter(UID = uid):
                post = Post.objects.get(UID = uid)
            post.titulo = request.POST["titulo"]
            post.resumo = request.POST["resumo"]
            post.conteudo = request.POST["conteudo"]
            post.blog = blog
            post.save()
            blog.posts.add(post)
            return redirect("Post",post.UID)
    else:
        return render(request, 'erro.html', {
            "msg":"Crie um conta antes de criar um blog!",
        })


def ExcluirPost(request, uid):
    if request.user.is_authenticated and Post.objects.filter(UID = uid):
        post = Post.objects.get(UID = uid)
        blog = post.blog
        if request.user == blog.dono:
            post.delete()
            return redirect("Blog", blog.UID)
        else:
            return render(request, 'erro.html', {
                "msg":"Você não tem permição para excluir o post!",
            })
    else:
        return render(request, 'erro.html', {
            "msg":"BLOG não encontrado!",
        })


def TodosBlogs(request):
    return render(request, 'todosBlogs.html', {
        "blogs": Blog.objects.all()
    })


def BlogView(request, uid):
    if Blog.objects.filter(UID = uid):
        blog = Blog.objects.get(UID = uid)
        return render(request, 'blog.html', {
            "blog":blog,
            "title":blog.nome
        })
    else:
        return render(request, 'erro.html', {
            "msg":"BLOG não encontrado!",
        })


def GETComentarios(lista, user):
    saida = []
    for c in lista:
        saida.append({
            "coment":c,
            "curtido":c.CheckLike(user)
        })
    return saida


def PostView(request, uid):
    if Post.objects.filter(UID = uid):
        post = Post.objects.get(UID = uid)
        if post.publicado or request.user == post.blog.dono:
            curtiu = False
            if request.user.is_authenticated:
                if Like.objects.filter(usuario = request.user, post=post):
                    curtiu = True
            return render(request, 'post.html', {
                "post":post,
                "title":post.titulo,
                "curtiu":curtiu,
                "comentarios":GETComentarios(post.GetComentarios(), request.user)
            })
        else:
            return render(request, 'erro.html', {
                "msg":"Visualização indisponivel!",
            })
    else:
        return render(request, 'erro.html', {
            "msg":"POST não encontrado!",
        })


def LikePost(request, uid):
    if request.user.is_authenticated and Post.objects.filter(UID = uid):
        post = Post.objects.get(UID = uid)
        if Like.objects.filter(post=post,usuario=request.user):
            like = Like.objects.get(post=post,usuario=request.user)
            like.delete()
        else:
            like = Like()
            like.post = post
            like.usuario = request.user
            like.save()
        return redirect("Post",uid)
    else:
        return render(request, 'erro.html', {
            "msg":"POST não encontrado!",
        })


def LikeComent(request, id):
    if request.user.is_authenticated and Comentario.objects.filter(pk = id):
        comentario = Comentario.objects.get(pk = id)
        if LikeComentario.objects.filter(comentario=comentario, usuario=request.user):
            like = LikeComentario.objects.get(comentario=comentario, usuario=request.user)
            like.delete()
        else:
            like = LikeComentario()
            like.comentario = comentario
            like.usuario = request.user
            like.save()
        return redirect("Post",comentario.post.UID)
    else:
        return render(request, 'erro.html', {
            "msg":"POST não encontrado!",
        })


def EditarPost(request, uid):
    if Post.objects.filter(UID = uid):
        post = Post.objects.get(UID = uid)
        if request.user == post.blog.dono and request.method == "GET":
            return render(request, 'Editar.html', {
                "post":post,
                "title":post.titulo
            })
        elif request.user == post.blog.dono and request.method == "POST":
            if request.POST["titulo"] and request.POST["resumo"] and request.POST["conteudo"]:
                post.titulo = request.POST["titulo"]
                post.resumo = request.POST["resumo"]
                post.conteudo = request.POST["conteudo"]
                post.save()
            return redirect("Post",post.UID)
        else:
            return render(request, 'erro.html', {
                "msg":"Erro na requesição!",
            })
    else:
        return render(request, 'erro.html', {
            "msg":"POST não encontrado!",
        })


def PublicarView(request, uid):
    if Post.objects.filter(UID = uid):
        post = Post.objects.get(UID = uid)
        if request.user == post.blog.dono:
            post.publicado = not post.publicado
            post.save()
            return redirect("Post",uid)
        else:
            return render(request, 'erro.html', {
                "msg":"Usuario não tem autorização!",
            })
    else:
        return render(request, 'erro.html', {
            "msg":"POST não encontrado!",
        })