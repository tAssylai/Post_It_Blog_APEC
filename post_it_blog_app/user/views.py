from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile


# ── Auth ──────────────────────────────────────────────────────────────────────

def loginsign(request):
    """Combined login / register page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        action = request.POST.get('action')  # 'login' or 'register'

        if action == 'login':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Invalid username or password.')

        elif action == 'register':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('home')

    return render(request, 'user/loginsign.html')


def logout_view(request):
    logout(request)
    return redirect('loginsign')


# ── Profile ───────────────────────────────────────────────────────────────────

@login_required
def profile(request):
    """Show the currently logged-in user's own profile."""
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    posts = request.user.posts.all()
    return render(request, 'user/profile.html', {
        'profile': profile_obj,
        'posts': posts,
    })


@login_required
def user_profile(request, username):
    """Show any user's public profile."""
    target_user = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=target_user)
    posts = target_user.posts.all()
    is_following = request.user.profile.following.filter(pk=profile_obj.pk).exists()
    return render(request, 'user/profile.html', {
        'profile': profile_obj,
        'posts': posts,
        'is_following': is_following,
        'is_own': target_user == request.user,
    })


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    their_profile, _ = Profile.objects.get_or_create(user=target_user)

    if my_profile.following.filter(pk=their_profile.pk).exists():
        my_profile.following.remove(their_profile)
    else:
        my_profile.following.add(their_profile)

    return redirect('user_profile', username=username)


# ── Settings ──────────────────────────────────────────────────────────────────

@login_required
def settings_view(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()
        avatar = request.FILES.get('avatar')

        profile_obj.bio = bio
        if avatar:
            profile_obj.avatar = avatar
        profile_obj.save()

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        messages.success(request, 'Settings saved.')
        return redirect('settings')

    return render(request, 'user/settings.html', {'profile': profile_obj})
