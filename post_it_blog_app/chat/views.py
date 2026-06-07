from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message


@login_required
def inbox(request):
    """List all conversations the current user is part of."""
    conversations = (
        request.user.conversations
        .prefetch_related('participants', 'messages')
        .order_by('-created_at')
    )
    return render(request, 'chat/messages.html', {'conversations': conversations})


@login_required
def conversation(request, conversation_id):
    """Open a specific conversation and send messages."""
    conv = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conv,
                sender=request.user,
                content=content,
            )
            # Mark unread messages from the other side as read
            conv.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
        return redirect('conversation', conversation_id=conv.id)

    messages_qs = conv.messages.select_related('sender').all()
    # Mark incoming messages as read when the user opens the chat
    conv.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    return render(request, 'chat/messages.html', {
        'conv': conv,
        'messages': messages_qs,
    })


@login_required
def start_conversation(request, username):
    """Start (or resume) a 1-on-1 conversation with another user."""
    other_user = get_object_or_404(User, username=username)

    # Find an existing 1-on-1 conversation between the two users
    conv = (
        Conversation.objects
        .filter(participants=request.user)
        .filter(participants=other_user)
        .first()
    )
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other_user)

    return redirect('conversation', conversation_id=conv.id)
