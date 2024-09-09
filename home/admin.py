from django.contrib import admin
from .models import Post, Comment, LibraryImages

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'body')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fields = ('author', 'title', 'image', 'body')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'comment')
    list_filter = ('user', 'blog')
    search_fields = ('comment', 'user__telegram_username')
    ordering = ('-id',)
    fields = ('user', 'blog', 'comment')

admin.site.register(LibraryImages)
