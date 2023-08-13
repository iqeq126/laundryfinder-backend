from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'content', 'tag_image')

admin.site.register(Tag, TagAdmin)