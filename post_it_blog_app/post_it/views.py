from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User

from .models import Post, Like, Comment, Follow, Profile


# -------------------------
# HOME
# -------------------------
@login_required
def home(request):
    user = request.user

    featured_posts = (
        Post.objects
        .select_related('author', 'author__profile')
        .prefetch_related('likes', 'comments')
        .annotate(like_count=Count('likes'))
        .order_by('-like_count', '-created_at')[:10]
    )

    recent_posts = (
        Post.objects
        .select_related('author', 'author__profile')
        .prefetch_related('likes', 'comments')
        .order_by('-created_at')[:20]
    )

    following_ids = Follow.objects.filter(
        follower=user
    ).values_list('following_id', flat=True)

    following_posts = (
        Post.objects
        .filter(author_id__in=following_ids)
        .select_related('author', 'author__profile')
        .prefetch_related('likes', 'comments')
        .order_by('-created_at')[:20]
    )

    following_users = User.objects.filter(id__in=following_ids)

    profile = None
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, 'post_it/index.html', {
        'profile': profile,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'following_posts': following_posts,
        'following_users': following_users,
    })


# -------------------------
# NEW POST
# -------------------------
@login_required
def newpost(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        title = request.POST.get('title', '').strip()
        image = request.FILES.get('image')

        if not content:
            messages.error(request, "Post content cannot be empty.")
            return redirect('newpost')

        if image and image.size > 5 * 1024 * 1024:
            messages.error(request, "Image too large.")
            return redirect('newpost')

        Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            image=image
        )

        return redirect('home')

    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, 'post_it/newpost.html', {
        'profile': profile
    })


# -------------------------
# LIKE
# -------------------------
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# -------------------------
# COMMENT
# -------------------------
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()

    if content:
        Comment.objects.create(
            author=request.user,
            post=post,
            content=content
        )

    return redirect(request.META.get('HTTP_REFERER', 'home'))