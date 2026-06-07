from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    notifs = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'post').order_by('-created_at')

    # Mark all as read when the page is opened
    notifs.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notifications.html', {'notifications': notifs})


@login_required
def mark_read(request, notif_id):
    Notification.objects.filter(id=notif_id, recipient=request.user).update(is_read=True)
    return redirect('notifications')
