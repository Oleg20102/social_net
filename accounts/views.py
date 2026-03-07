from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render

from posts.models import Post
from posts.forms import PostForm

from .models import User
from .forms import CustomUserCreationForm

@login_required
def home_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    posts = Post.objects.select_related("author").all()
    return render(request, "home.html", {"form": form, "posts": posts})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {'profile_user': user})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile", username=user.username)
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})

User = get_user_model()

@login_required
def user_search(request):
    q = request.GET.get("q", "").strip()
    results = []

    if q:
        results = User.objects.filter(username__icontains=q).exclude(id=request.user.id)[:30]

    return render(request, "accounts/search.html", {"q": q, "results": results})
