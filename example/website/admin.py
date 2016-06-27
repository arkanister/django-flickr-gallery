from django.contrib import admin
from example.website.forms import ArticleAdminForm
from example.website.models import Article


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
