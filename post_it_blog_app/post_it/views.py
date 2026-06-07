from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like, Comment


def home(request):
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    return render(request, 'post_it/index.html', {'posts': posts})


@login_required
def newpost(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        title = request.POST.get('title', '').strip()
        image = request.FILES.get('image')

        if not content:
            messages.error(request, 'Post content cannot be empty.')
            return render(request, 'post_it/newpost.html')

        Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            image=image,
        )
        messages.success(request, 'Post created!')
        return redirect('home')

    return render(request, 'post_it/newpost.html')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()
    if content:
        Comment.objects.create(author=request.user, post=post, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
