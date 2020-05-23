from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from home.models import Post


def picture_list(request):
    page = request.GET.get('page', 1)
    object_list = Post.objects.all().order_by('-created')
    paginator = Paginator(object_list, 24)
    objects = paginator.get_page(page)
    return render(request, 'allpictures/picture_list.html', context={"objects": objects})
