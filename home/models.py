from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from markdown import markdown
from markdownx.models import MarkdownxField

from multiphoto.models import MultiPhoto


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/home/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=CASCADE)
    image = models.ImageField(upload_to='home/%Y/%m/%d/', blank=False)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return '/home/{}/'.format(self.pk)

    def get_post_update_url(self):
        return self.get_absolute_url() + 'update/'


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    like_posts = models.ManyToManyField(Post, blank=True)

    def __int__(self):
        return self.user

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE)
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
