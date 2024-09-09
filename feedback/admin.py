from django.contrib import admin
from .models import Feedback, About, ImageAbout
from unfold.admin import ModelAdmin


@admin.register(Feedback)
class FeedbackAdminClass(ModelAdmin):
    pass

admin.site.register(About)
admin.site.register(ImageAbout)

