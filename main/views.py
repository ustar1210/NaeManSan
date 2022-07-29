from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from study.models import *
from study.models import study
from django.utils import timezone

# Create your views here.


def showmain(request):
    posts = study.objects.all()
    return render(request, 'main/index.html', {
        'posts':posts,
    })


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def pricing(request):
    return render(request, 'main/pricing.html')


def worksingle(request):
    return render(request, 'main/work-single.html')


def work(request):
    return render(request, 'main/work.html')


def studying(request):
    diarys = Diary.objects.all()
    all_dates = StudyDate.objects.all()
    return render(request, 'main/studying.html', {'diarys': diarys, 'all_dates': all_dates})


def plan(request):
    plans = Plan.objects.all()
    return render(request, 'main/plan.html', {'plans': plans})


def plan_detail(request, id):
    plan = get_object_or_404(Plan, pk=id)
    all_comments = plan.comments.all().order_by('-created_at')
    return render(request, 'main/plan_detail.html', {'plan': plan, 'comments': all_comments})


def plan_new(request):
    return render(request, 'main/plan_new.html')


def plan_create(request):
    new_plan = Plan()
    new_plan.title = request.POST['title']
    new_plan.writer = request.POST['writer']
    new_plan.pub_date = timezone.now()
    new_plan.body = request.POST['body']
    new_plan.image = request.FILES.get('image')
    new_plan.save()
    return redirect('main:plan_detail', new_plan.id)


def plan_edit(request, id):
    edit_plan = Plan.objects.get(id=id)
    return render(request, 'main/plan_edit.html', {'plan': edit_plan})


def plan_update(request, id):
    update_plan = get_object_or_404(Plan, id=id)
    update_plan.title = request.POST['title']
    update_plan.writer = request.POST['writer']
    update_plan.pub_date = timezone.now()
    update_plan.body = request.POST['body']
    update_plan.save()
    return redirect('main:plan_detail', update_plan.id)


def plan_delete(request, id):
    delete_plan = Plan.objects.get(id=id)
    delete_plan.delete()
    return redirect('main:plan')


def create_comment(request, plan_id):
    if request.method == "POST":
        plan = get_object_or_404(Plan, pk=plan_id)
        current_user = request.user
        comment_content = request.POST.get('content')
        Comment.objects.create(content=comment_content,
                               writer=current_user, plan=plan)
    return redirect('main:plan_detail', plan_id)


def edit_comment(request, comment_id):
    edit_comment = Comment.objects.get(id=comment_id)
    return render(request, 'main/edit_comment.html', {'comment': edit_comment})


def update_comment(request, comment_id):
    update_comment = get_object_or_404(Comment, pk=comment_id)
    update_comment.writer = request.user
    update_comment.content = request.POST['content']
    update_comment.save()
    return redirect('main:plan_detail', update_comment.plan.id)


def delete_comment(request, comment_id):
    delete_comment = get_object_or_404(Comment, pk=comment_id)
    delete_comment.delete()
    return redirect('main:plan_detail', delete_comment.plan.id)


# 스터디 일지 CRUD

def diary_detail(request, id):
    diary = get_object_or_404(Diary, pk=id)
    return render(request, 'main/diary_detail.html', {'diary': diary})


def diary_new(request):
    return render(request, 'main/diary_new.html')


def diary_create(request):
    new_diary = Diary()
    new_diary.title = request.POST['title']
    new_diary.writer = request.POST['writer']
    new_diary.date = request.POST['date']
    new_diary.pub_date = timezone.now()
    new_diary.body = request.POST['body']
    new_diary.image = request.FILES.get('image')
    new_diary.save()
    return redirect('main:diary_detail', new_diary.id)


def studydate_create(request):
    new_date = StudyDate()
    new_date.content = request.POST['content']
    new_date.pub_date = timezone.now()
    new_date.save()
    return redirect('main:studying')
