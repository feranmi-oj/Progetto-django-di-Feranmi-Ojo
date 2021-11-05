from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView, ListView, UpdateView,DeleteView
from .forms import ArticleEditForm
from .models import Article
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import hashlib
from .utils import sendTransaction

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
@method_decorator(cache_page(CACHE_TTL),  name='dispatch')

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context



class ArticleListView(ListView):
    model = Article
    paginate_by = 5
    def get_queryset(self):
        tag = self.kwargs.get('category_tag', None)
        queryset = Article.objects.filter(status='PUBLISHED')
        if tag:
            c = tag
            queryset = Article.objects.filter(status='PUBLISHED').filter(category__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Article.CATEGORIES
        tag = self.kwargs.get('category_tag', None)
        context['tag'] = tag
        return context



@login_required
def article_new(request):
    if request.method == "POST":
        forbiddenword = "hack"
        form = ArticleEditForm(request.POST, request.FILES,)
        if  forbiddenword not in request.POST['content']:
            if forbiddenword not in request.POST['title'] and form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published = timezone.now()
                post.writeOnChain()
                post.save()
                return redirect(f'/articles/{post.slug}/',messages.success(request,"The post was successfully published "))
            else:
                messages.error(request,"The data entered is not valid, remember that the word 'hack' is prohibited in the post ")

        else:
            messages.error(request,"The data entered is not valid, remember that the word 'hack' is prohibited in the post ")

    else:
        form = ArticleEditForm()

    return render(request, 'articles/article_new.html', {'form': form}, )


class UpdateArticleView(UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'articles/article_edit.html'
    def form_valid(self, form):
        forbiddenword = "hack"
        if  forbiddenword not in self.request.POST['content'] :
            if forbiddenword not in self.request.POST['title']:
                form.instance.author = self.request.user
                messages.success(self.request, "The post was successfully edited ")
                return super().form_valid(form)
            else:
                messages.error(self.request,"The data entered is not valid, remember that the word 'hack' is prohibited in the post ")
        else:
            messages.error(self.request,"The data entered is not valid, remember that the word 'hack' is prohibited in the post ")
        return render(self.request, 'articles/article_edit.html', {'form': form}, )


class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy("blog:blog")


def page_user_admin(request):
    users = User.objects.all().annotate(post_count=Count('article'))
    context = {'users': users}
    return render(request, 'articles/page_administration.html',  context)


def search(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/search/")
        posts = Article.objects.filter(content__icontains=querystring)
        context = {"posts": posts, "querystring": querystring}
        return render(request, "articles/search.html", context)
    else:
        return render(request, "articles/search.html")



def posts(request):
    response = []
    posts = Article.objects.filter().order_by('published')
    for post in posts:
        response.append(
            {
                'published' :f"{post.published}",
                'title':f"{post.title}",
                'slug':f"{post.slug}",
                'author':f"{post.author}",
                'content':f"{post.content}",
                'image':f"{post.img}",
                'created':f"{post.created}",
                'updated':f"{post.updated}",
                'hash': f"{post.hash}",
                'txId': f"{post.txId}"
            }
        )
    return JsonResponse(response, safe=False,json_dumps_params={'indent': 2})

def post_ultima_ora(request):
    response= []
    dt = now()
    posts_last_hour1= Article.objects.filter(published__range=(dt-timedelta(hours=1), dt))
    for post in posts_last_hour1:
        response.append(
            {
                'published' :f"{post.published}",
                'title':f"{post.title}",
                'slug':f"{post.slug}",
                'author':f"{post.author}",
                'content':f"{post.content}",
                'image':f"{post.img}",
                'created':f"{post.created}",
                'updated':f"{post.updated}",
                'hash': f"{post.hash}",
                'txId': f"{post.txId}"
            }
        )
    return JsonResponse(response, safe=False,json_dumps_params={'indent': 2})
