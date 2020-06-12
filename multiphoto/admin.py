from django.contrib import admin

# Register your models here.
from multiphoto.models import MultiPhoto, Image, MultiComment


admin.site.register(MultiPhoto)
admin.site.register(MultiComment)
admin.site.register(Image)
