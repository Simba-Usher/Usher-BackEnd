from django.db import models
from user.models import *
from django.conf import settings

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class ComPost(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    comcomments_cnt = models.PositiveIntegerField(default=0)
    category_choices = [
        ('자유', '자유'), 
        ('질문', '질문'), 
        ('에디터 픽', '에디터 픽'),
        ('공지', '공지'),
    ]
    category = models.CharField(default='', max_length = 10, choices=category_choices, blank=False, null=False)

class ComComment(models.Model):
    id = models.AutoField(primary_key=True)
    compost= models.ForeignKey(ComPost, blank=True, null=True, on_delete=models.CASCADE, related_name='comcomments')
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #like = models.PositiveIntegerField(default=0)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)

    def save(self, *args, **kwargs):
        # 댓글이 생성될 때 'comcomments_cnt' 필드 갱신
        self.compost.comcomments_cnt = self.compost.comcomments.count()
        self.compost.save()
        super(ComComment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 댓글이 삭제될 때 'comcomments_cnt' 필드 갱신
        self.compost.comcomments_cnt = self.compost.comcomments.count()
        self.compost.save()
        super(ComComment, self).delete(*args, **kwargs)

class CommunityReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("heart", "Heart"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ComReply(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    comcomment = models.ForeignKey(ComComment, blank=False, null=False, on_delete=models.CASCADE, related_name='comreplies')

#class ComPostMedia(models.Model):
#    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE, related_name='media')
#    media = models.ImageField(upload_to='compost_media/', blank=True, null=True)
