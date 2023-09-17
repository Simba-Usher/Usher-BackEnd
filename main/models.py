from django.db import models
from django.conf import settings
from user.models import CustomUser
from mypage.models import Ticket
from datetime import date

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class MainPost(models.Model):
    id = models.AutoField(primary_key=True)
    liked_users = models.ManyToManyField(CustomUser, related_name="liked_mainposts", blank=True)
    title = models.CharField(max_length=50)
    place = models.CharField(max_length=30, blank=True, null=True)
    sentence = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to='mainpost_media', blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    start_date = models.DateField(verbose_name='시작날짜', null=True)
    end_date = models.DateField(verbose_name='종료날짜', null=True)
    mainreviews_cnt = models.PositiveIntegerField(default=0)
    GENRE_CHOICES = [
        ('뮤지컬', '뮤지컬'),
        ('연극', '연극'),
        ('클래식', '클래식'),
        ('무용', '무용'),
        ('콘서트', '콘서트'),
        ('가족', '가족')
    ]

    LOCATION_CHOICES = [
        ('서울', '서울'),
        ('경기', '경기'),
        ('인천', '인천'),
        ('강원', '강원'),
        ('충청', '충청'),
        ('경상', '경상'),
        ('전라', '전라'),
        ('제주', '제주')
    ]

    genre = models.CharField(
        max_length=10,
        choices=GENRE_CHOICES,
        default='뮤지컬',
    )
    
    location = models.CharField(
        max_length=10,
        choices=LOCATION_CHOICES,
        default='서울',
    )

    def __str__(self):
        return self.title
    

class MainReview(models.Model):
    id = models.AutoField(primary_key=True)
    mainpost= models.ForeignKey(MainPost, blank=True, null=True, on_delete=models.CASCADE, related_name='mainreviews')
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='mainreviews')
    #writer = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, blank=False, null=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True, related_name='mainreviews')
    RATING_CHOICES = [
        (1, '1점'),
        (2, '2점'),
        (3, '3점'),
        (4, '4점'),
        (5, '5점'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    mainrecoms_cnt = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # 댓글이 생성될 때 'comcomments_cnt' 필드 갱신
        self.mainpost.mainreviews_cnt = self.mainpost.mainreviews.count()
        self.mainpost.save()
        super(MainReview, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 댓글이 삭제될 때 'comcomments_cnt' 필드 갱신
        self.mainpost.mainreviews_cnt = self.mainpost.mainreviews.count()
        self.mainpost.save()
        super(MainReview, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.rating}점 - {self.content[:10]}"

    class Meta:
        verbose_name = "MainReview"
        verbose_name_plural = "MainReviews"

class MainPostReaction(models.Model):
    REACTION_CHOICES = (("like", "like"), ("heart", "Heart"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    mainpost = models.ForeignKey(MainPost, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class MainReviewReaction(models.Model):
    REACTION_CHOICES = (("공감", "공감"), ("heart", "Heart"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    mainreview = models.ForeignKey(MainReview, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class MainReviewComment(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    mainreview = models.ForeignKey(MainReview, blank=False, null=False, on_delete=models.CASCADE, related_name='mainrecoms')

