from django.contrib import admin
from .models import Review, Comment

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = '__all__'

class CommentAdmin(admin.ModelAdmin):
    list_display = '__all__'