from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date')
    date_hierarchy = 'creation_date'
