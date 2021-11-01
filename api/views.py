from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime' : post.datetime,
                'content' : post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash' : post.hash,
                'txId' : post.txId
            }
        )
    return JsonResponse(response, safe=False)
# Create your views here.
def newPost(request):
    pass