from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class study(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE)  # 작성자, User 모델 사용
    name = models.CharField(max_length=50)  # 스터디명
    intro = models.CharField(max_length=100)  # 스터디 한줄 소개
    body = models.TextField()  # 스터디 정보
    phnum = models.CharField(max_length=13)  # 대표자 연락처
    # 스터디 난이도(빡센 정도 1~10으로 입력받을 예정)
    difficulty = models.IntegerField(default=0)

    image = models.FileField(
        upload_to="image/", null=True
    )  # 스터디 관련 이미지(있으면 글 썸네일, 없으면 메인 로고가 글 썸네일)
#-----------------좋아요------------------#
    like_user_set = models.ManyToManyField(User, blank=True, related_name='likes_user_set',through='Like')

    @property
    def like_count(self):
        return self.like_user_set.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(study, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =(('user', 'study'))
#-----------------좋아요------------------#

# 스터디 일정
class todo(models.Model):
    date = models.DateField()
    content = models.TextField()
    post = models.ForeignKey(
        study, on_delete=models.CASCADE, related_name='todos')

# 스터디 출석체크


class check(models.Model):
    date = models.DateTimeField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        study, on_delete=models.CASCADE, related_name='checks')


class notion(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        study, on_delete=models.CASCADE, related_name='notions')


class Daily(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    body = models.TextField()
    date = models.CharField(max_length=30)
    image = models.ImageField(upload_to="daily/", blank=True, null=True)
    post = models.ForeignKey(
        study, on_delete=models.CASCADE, related_name='dailys')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:20]
