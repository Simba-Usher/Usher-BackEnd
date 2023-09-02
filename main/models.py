from django.db import models
from user.models import CustomUser

class MainPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    #image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    reviews_cnt = models.PositiveIntegerField(default=0)
    GENRE_CHOICES = [
        ('뮤지컬', '뮤지컬'),
        ('연극', '연극'),
        ('클래식', '클래식'),
        ('무용', '무용'),
        ('콘서트', '콘서트'),
        ('아동/가족', '아동/가족')
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

    genre_type = models.CharField(
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
    mainpost= models.ForeignKey(MainPost, blank=True, null=True, on_delete=models.CASCADE, related_name='comcomments')
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #like = models.PositiveIntegerField(default=0)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    RATING_CHOICES = [
        (1, '1점'),
        (2, '2점'),
        (3, '3점'),
        (4, '4점'),
        (5, '5점'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES, default=5)

    def save(self, *args, **kwargs):
        # 댓글이 생성될 때 'comcomments_cnt' 필드 갱신
        self.mainpost.mainreviews_cnt = self.mainpost.mainreviews.count()
        self.mainpost.save()
        super(MainReview, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 댓글이 삭제될 때 'comcomments_cnt' 필드 갱신
        self.mainpost.mainreviews = self.mainpost.mainreviews.count()
        self.mainpost.save()
        super(MainReview, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.rating}점 - {self.comment[:10]}"  
        
    class Meta:
        verbose_name = "MainReview"
        verbose_name_plural = "MainReviews"
