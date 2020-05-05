from django.contrib import admin
from django.conf import settings

from . import models

# Register your models here.
if settings.DEBUG:
    @admin.register(models.Post)
    class PostAdmin(admin.ModelAdmin):
        fields = ('title', 'content', 'hash_tags', 'picture', 'date')

        def save_model(self, request, obj, form, change):
            obj.created_by = request.user
            super().save_model(request, obj, form, change)
else:
    @admin.register(models.Post)
    class PostAdmin(admin.ModelAdmin):
        fields = ('title', 'content', 'hash_tags', 'picture')

        def save_model(self, request, obj, form, change):
            obj.created_by = request.user
            super().save_model(request, obj, form, change)