from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import CASCADE
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from markdown import markdown
from markdownx.models import MarkdownxField


class MultiPhoto(models.Model):
    title = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return '/multi/{}/'.format(self.pk)


class Image(models.Model):
    post = models.ForeignKey(MultiPhoto, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to='multi/images',  # 저장 위치
        processors=[ResizeToFit(width=750)],  # 처리할 작업 목록
        format='JPEG',  # 저장 포맷(확장자)
        options={'quality': 90},  # 저장 포맷 관련 옵션 (JPEG 압축률 설정)
    )


class MultiComment(models.Model):
    post = models.ForeignKey(MultiPhoto, on_delete=CASCADE)
    author = models.ForeignKey(User, on_delete=CASCADE)
    text = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)

    def __str__(self):
        return '{}'.format(self.text)
