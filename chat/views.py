from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Message
from django.db.models import Q, Count

@login_required
def inbox(request):
    query = request.GET.get("q")

    users = User.objects.filter(
        sent_messages__receiver=request.user
    ).distinct() | User.objects.filter(
        received_messages__sender=request.user
    ).distinct()

    users = users.exclude(id=request.user.id)

    # якщо є пошуковий запит
    search_results = None
    if query:
        search_results = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    return render(request, "chat/inbox.html", {
        "users": users,
        "search_results": search_results,
        "query": query,
    })

User = get_user_model()


@login_required
def room(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("created_at")
    
    Message.objects.filter(
    sender=other_user,
    receiver=request.user,
    is_read=False
).update(is_read=True)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )
            return redirect("chat_room", username=other_user.username)

    return render(request, "chat/room.html", {
        "other_user": other_user,
        "messages": messages
    })
