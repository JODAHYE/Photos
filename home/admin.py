from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from home.models import Post, Category, Comment, Profile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Profile)