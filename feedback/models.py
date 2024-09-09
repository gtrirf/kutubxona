from django.db import models
from users.models import CustomUser as User
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks',
        verbose_name='User'
    )
    message = models.TextField(verbose_name='Message')
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ],
        verbose_name='Rating'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-created_at']

    def __str__(self):
        return f'Feedback by {self.user} with rating {self.rating}'



class About(models.Model):
    body = models.TextField()   
    theme = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'about'

    def __str__(self):
        return self.theme


class ImageAbout(models.Model):
    image = models.ImageField()
    about = models.ForeignKey(About, on_delete=models.CASCADE)

    class Meta:
        db_table = 'imagesforabout'

    def __str__(self):
        return f'image for about {self.about.theme}'
    
