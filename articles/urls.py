"""
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('list/<slug:category_tag>/', views.ArticleListView.as_view(), name='article-list'),
    path('<slug:slug>/',views.ArticleDetailView.as_view() , name='article-detail'),
    path('article/new/', views.article_new, name='article-new'),
    path('article/edit/<slug:slug>/', views.UpdateArticleView.as_view(), name='article-edit'),
    path('article/<slug:slug>/delete/', views.DeleteArticleView.as_view(), name='article-delete'),
    path('page/administration', views.page_user_admin, name='page_administration'),
    path('allpost-json', views.posts, name='allposts-json'),
    path('postsLastHour', views.post_ultima_ora, name='posts-last-hour'),
    path('search', views.search, name="search"),


]
