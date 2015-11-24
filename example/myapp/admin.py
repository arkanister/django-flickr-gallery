from django.contrib import admin
from example.myapp.forms import ArticleAdminForm
from example.myapp.models import Article


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
