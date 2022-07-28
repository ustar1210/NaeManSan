from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class study(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자, User 모델 사용
    name = models.CharField(max_length=50)  # 스터디명
    section = models.CharField(max_length=30)  # 분야
    intro = models.CharField(max_length=100)  # 스터디 한줄 소개
    qualification = models.CharField(max_length=100)  # 스터디 참가 대상
    member_start = models.IntegerField(default=1)  # 모집 인원 시작
    member_end = models.IntegerField(default=1)  # 모집 인원 끝
    start_date = models.DateField()  # 활동 기간(시작일)
    due_date = models.DateField()  # 활동 기간(마감일
    body = models.TextField()  # 스터디 정보
    body = models.TextField()  # 스터디 정보
    difficulty = models.IntegerField(default=0)  # 스터디 난이도(빡센 정도 1~10으로 입력받을 예정)
    phnum = models.CharField(max_length=13)  # 대표자 연락처
    image = models.FileField(
        upload_to="image/", null=True
    )  # 스터디 관련 이미지(있으면 글 썸네일, 없으면 메인 로고가 글 썸네일)
    study_member_request = models.ManyToManyField(
        User, related_name="study_member_request", through="member_request"
    )  # 가입신청 유저들
    study_member = models.ManyToManyField(
        User, related_name="study_member", through="member"
    )  # 가입된 유저들
    is_over = models.BooleanField()


class member_request(models.Model):
    study = models.ForeignKey(study, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class member(models.Model):
    study = models.ForeignKey(study, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# 스터디 일정
class todo(models.Model):
    date = models.DateField()
    content = models.TextField()
    post = models.ForeignKey(study, on_delete=models.CASCADE, related_name='todos')

#스터디 출석체크
class check(models.Model):
    date = models.DateTimeField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(study, on_delete=models.CASCADE, related_name='checks')

class notion(models.Model):
    content = models.TextField()
    post = models.ForeignKey(study, on_delete=models.CASCADE, related_name='notions')

class Daily(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    body = models.TextField()
    date = models.CharField(max_length=30)
    image = models.ImageField(upload_to="daily/", blank = True, null = True)
    post = models.ForeignKey(study, on_delete=models.CASCADE, related_name='dailys')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:20]