from django.shortcuts import render, get_object_or_404
from .models import Content

def post_list(request):
    posts = Content.objects.all()  # Ensure this matches the context key
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Content, pk=pk)  # Ensure this matches the context key
    return render(request, 'post_detail.html', {'post': post})

