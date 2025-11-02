from django.contrib import admin
from myapp.models import *

# Register your models here.


admin.site.register(MyUser)
admin.site.register(HeaderSettings)
admin.site.register(NavMenu)
admin.site.register(TrendingTag)
# admin.site.register(articale_master)



# app/admin.py
from django.contrib import admin
from .models import articale_master, Comment

@admin.register(articale_master)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'is_trending')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'content', 'article__title')














    



