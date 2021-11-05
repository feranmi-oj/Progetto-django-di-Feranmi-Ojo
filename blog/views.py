from django.shortcuts import render,redirect
from django.views.generic.base import  TemplateView
from django.core.paginator import Paginator
from articles.models import Article






class BlogView(TemplateView):
    template_name = 'blog/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles =Article.objects.filter(status='PUBLISHED')
        context['banner'] =articles[0]
        articles_list =articles[1:]
        context['articles_list'] = articles_list
        paginator = Paginator(articles_list,5)
        page_number= self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['categories']= Article.CATEGORIES
        return context

