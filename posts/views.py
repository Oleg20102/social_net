from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Post

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # щоб можна було видаляти тільки СВІЙ пост
    if post.author != request.user:
        messages.error(request, "Ти не можеш видаляти чужі пости 😅")
        return redirect("home")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Пост видалено ✅")
        return redirect("home")

    # якщо хтось відкриє delete по GET — просто назад
    return redirect("home")
@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("home")
