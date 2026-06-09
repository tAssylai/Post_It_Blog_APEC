from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from post_it.models import Profile
from django.views.decorators.http import require_POST


# ── AUTH ─────────────────────────────────────────────

def loginsign(request):
    if request.user.is_authenticated:
        return redirect('home')

    action = request.POST.get('action', 'register')

    if request.method == 'POST':
        if action == 'login':
            username = request.POST.get('login_username', '').strip()   # <-- CHANGED
            password = request.POST.get('login_password', '')           # <-- CHANGED

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Invalid username or password.')

        elif action == 'register':
            username = request.POST.get('reg_username', '').strip()    # <-- CHANGED
            email = request.POST.get('email', '').strip()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('home')

        # If we reach here, an error occurred – pass the action back
        return render(request, 'user/loginsign.html', {'action': action})

    # GET request
    return render(request, 'user/loginsign.html', {'action': action})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('loginsign')


# ── PROFILE ─────────────────────────────────────────

@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    posts = request.user.posts.all() if hasattr(request.user, "posts") else []

    return render(request, 'user/profile.html', {
        'profile': profile_obj,
        'posts': posts,
        'is_own': True,
    })


@login_required
def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=target_user)

    posts = target_user.posts.all() if hasattr(target_user, "posts") else []

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


# ── SETTINGS ─────────────────────────────────────────

@login_required
def settings_view(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_obj.bio = request.POST.get('bio', '').strip()
        profile_obj.display_name = request.POST.get('display_name', '').strip()

        avatar = request.FILES.get('avatar')
        if avatar:
            profile_obj.avatar = avatar

        profile_obj.save()

        request.user.email = request.POST.get('email', '').strip()
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.save()

        messages.success(request, 'Settings saved.')
        return redirect('settings')

    return render(request, 'user/settings.html', {
        'profile': profile_obj
    })