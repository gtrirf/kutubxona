from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from users.models import CustomUser as User

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Author'
    )
    title = models.CharField(max_length=255, verbose_name='Title')
    image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        verbose_name='Image'
    )
    body = RichTextField(verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('home:blog-detail', args=[str(self.pk)])
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    blog = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Blog Post'
    )
    comment = models.TextField(verbose_name='Comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',verbose_name='User')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user} on {self.blog}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.blog.pk})


class LibraryImages(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'images'

    def __str__(self):
        return self.name

