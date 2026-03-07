from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupCreateForm
from .models import Group, GroupMessage

@login_required
def delete_group(request, slug):
    group = get_object_or_404(Group, slug=slug)

    # тільки творець може видалити
    if request.user != group.creator:
        return redirect("group_detail", slug=slug)

    group.delete()
    return redirect("group_list")

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)

    is_member = request.user in group.members.all()

    # Якщо натиснули "Приєднатись"
    if request.method == "POST" and "join_group" in request.POST:
        group.members.add(request.user)
        return redirect("group_detail", pk=pk)

    # Якщо пишуть повідомлення
    if request.method == "POST" and "send_message" in request.POST:
        if is_member:
            content = request.POST.get("content")
            if content:
                GroupMessage.objects.create(
                    group=group,
                    author=request.user,
                    content=content
                )
        return redirect("group_detail", pk=pk)

    messages = group.messages.all()

    return render(request, "groups/group_detail.html", {
        "group": group,
        "messages": messages,
        "is_member": is_member,
    })



@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, "groups/group_list.html", {"groups": groups})


@login_required
def create_group(request):
    form = GroupCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        group = form.save(commit=False)
        group.creator = request.user
        group.save()
        group.members.add(request.user)
        return redirect("group_detail", slug=group.slug)

    return render(request, "groups/create_group.html", {"form": form})

@login_required
def group_detail(request, slug):
    group = Group.objects.get(slug=slug)

    is_member = request.user in group.members.all()

    messages = GroupMessage.objects.filter(group=group).order_by("created_at")

    # ПРИЄДНАННЯ ДО ГРУПИ
    if request.method == "POST" and "join_group" in request.POST:
        group.members.add(request.user)
        return redirect("group_detail", slug=group.slug)

    # ВІДПРАВКА ПОВІДОМЛЕННЯ
    if request.method == "POST" and "send_message" in request.POST and is_member:
        content = request.POST.get("content")

        if content:
            GroupMessage.objects.create(
                group=group,
                author=request.user,
                content=content
            )

        return redirect("group_detail", slug=group.slug)

    return render(request, "groups/group_detail.html", {
        "group": group,
        "is_member": is_member,
        "messages": messages
    })


@login_required
def join_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group.members.add(request.user)
    return redirect("group_detail", slug=slug)


@login_required
def leave_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group.members.remove(request.user)
    return redirect("group_list")