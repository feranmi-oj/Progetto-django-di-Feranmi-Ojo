from django.contrib import admin

# Register your models here.
from django.contrib import admin
from.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title','author','created','published','updated')
    list_filter = ('created','author')
    search_fields = ('title','content')
    ordering = ('created','published')
