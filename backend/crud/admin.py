from django.contrib import admin
from .models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.get_fields() if not field.many_to_many]# ("product_name", "user", "description", 'tag_list')
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tag')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt', 'tag_list')
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# admin.site.register(Product, ProductAdmin)
