from django.shortcuts import render, redirect, get_object_or_404

from main.models import Diary
from .models import check, study, todo, notion, Daily
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import ListView
from django.core.paginator import Paginator

# Create your views here.

#-----------------좋아요------------------#
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import Like
from django.contrib.auth.decorators import login_required
import json

@require_POST
@login_required
def like_toggle(request, study_id):
    Study = get_object_or_404(study, pk = study_id)
    study_like, study_like_created = Like.objects.get_or_create(user=request.user, study=Study)

    if not study_like_created:
        study_like.delete()
        result = "like_cancel"
    else:
        result = "like"
    context = {
        "like_count" : Study.like_count,
        "result" : result
    }
    return HttpResponse(json.dumps(context), content_type = "application/json")
#-----------------좋아요------------------#


def studylist(request):
    posts = study.objects.all()
    return render(request, "study/studylist.html", {"posts": posts})


def new(request):
    return render(request, "study/new.html")


def create(request):
    new_study = study()
    new_study.writer = request.user
    new_study.name = request.POST["name"]

    new_study.intro = request.POST["intro"]

    new_study.body = request.POST["body"]
    new_study.difficulty = request.POST["difficulty"]

    new_study.image = request.FILES.get("image")

    new_study.save()

    return redirect("study:detail", new_study.id)


def apply_study(request, id):
    cur_study = study.objects.get(id=id)
    is_apply = request.user in cur_study.study_member_request.all()  # 지원 여부 확인
    if is_apply:  # 지원 취소
        cur_study.study_member_request.remove(request.user)
    else:  # 지원
        cur_study.study_member_request.add(request.user)

    return redirect("study:detail", cur_study.id)


def accept_request(request, study_id, user_id):
    request_user = get_object_or_404(User, pk=user_id)
    cur_study = study.objects.get(id=study_id)
    cur_study.study_member_request.remove(request_user)  # 대기 멤버에서 제거
    cur_study.study_member.add(request_user)  # 멤버에 추가

    return redirect("study:detail", cur_study.id)


def refuse_request(request, study_id, user_id):
    request_user = get_object_or_404(User, pk=user_id)
    cur_study = study.objects.get(id=study_id)
    cur_study.study_member_request.remove(request_user)  # 대기 멤버에서 제거

    return redirect("study:detail", cur_study.id)


def recruit_over(request, id):
    cur_study = study.objects.get(id=id)
    cur_study.is_over = True
    cur_study.study_member_request.clear()  # 마감할거니까 혹시라도 가입요청 있으면 다 지워
    cur_study.save()

    return redirect("study:detail", cur_study.id)


def detail(request, id):
    post = get_object_or_404(study, pk=id)
    todos = post.todos.all()
    checks = post.checks.all()
    dailys = post.dailys.all()
    notions_all = notion.objects.all().order_by("-id")
    page = int(request.GET.get("p", 1))  # 없으면 1로 지정
    paginator = Paginator(notions_all, 5)
    notions = paginator.get_page(page)
    # is_author : 현재 접속한 유저가 수정하려는 스터디의 작성자인지 확인하고 저장
    if request.user == post.writer:
        is_author = True
    else:
        is_author = False

    return render(
        request,
        "study/detail.html",
        {
            "post": post,
            "is_author": is_author,
            "todos": todos,
            "checks": checks,
            "notions": notions,
            "dailys": dailys,
        },
    )


def edit(request, id):
    edit_study = study.objects.get(id=id)
    # is_author : 현재 접속한 유저가 수정하려는 스터디의 작성자인지 확인하고 저장
    if request.user == edit_study.writer:
        is_author = True
    else:
        is_author = False

    return render(
        request, "study/edit.html", {"post": edit_study,
                                     "is_author": is_author}
    )


def update(request, id):
    update_study = study.objects.get(id=id)
    update_study.writer = request.user
    update_study.name = request.POST["name"]
    # update_study.section = request.POST["section"]
    update_study.intro = request.POST["intro"]
    update_study.body = request.POST["body"]
    update_study.difficulty = request.POST["difficulty"]
    if request.FILES.get("image"):  # 이미지가 새로 들어오지 않으면 건드리지 않음
        update_study.image = request.FILES.get("image")
    update_study.save()

    return redirect("study:detail", update_study.id)


def delete(request, id):
    delete_study = study.objects.get(id=id)
    delete_study.delete()

    return redirect("study:studylist")


def create_todo(request, study_id):
    new_todo = todo()
    new_todo.date = request.POST["todo_date"]
    new_todo.content = request.POST["todo_content"]
    new_todo.post = get_object_or_404(study, pk=study_id)
    new_todo.save()
    return redirect("study:detail", study_id)


def create_check(request, study_id):
    new_check = check()
    new_check.date = timezone.now()
    new_check.writer = request.user
    new_check.post = get_object_or_404(study, pk=study_id)
    new_check.save()
    return redirect("study:detail", study_id)


def create_notion(request, study_id):
    new_notion = notion()
    new_notion.content = request.POST["notion_content"]
    new_notion.post = get_object_or_404(study, pk=study_id)
    new_notion.save()
    return redirect("study:detail", study_id)


def daily_detail(request, study_id, daily_id):
    post = get_object_or_404(study, pk=study_id)
    daily = Daily.objects.get(id=daily_id)
    return render(request, 'study/daily_detail.html', {'post': post, 'daily': daily})


def daily_new(request, study_id):
    post = get_object_or_404(study, pk=study_id)
    return render(request, 'study/daily_new.html', {'post': post})


def daily_create(request, study_id):
    new_daily = Daily()
    new_daily.post = get_object_or_404(study, pk=study_id)
    new_daily.title = request.POST['title']
    new_daily.writer = request.POST['writer']
    new_daily.date = request.POST['date']
    new_daily.pub_date = timezone.now()
    new_daily.body = request.POST['body']
    new_daily.image = request.FILES.get('image')
    new_daily.save()
    return redirect('study:detail', study_id)
