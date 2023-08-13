from django.db import models
# from .models import Tag, TagImage
# from crud.models import Product

# from skimage.measure.fit import BaseModel

# 이미지 업로드 경로
def image_upload_path(instance, filename):
    return f'{instance}/{filename}'
"""
class TagImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=image_upload_path)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'tag_image'
"""
# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=255)
    to_date = models.DateField()
    content = models.TextField()
    status = models.CharField(max_length=2)
    tag_image = models.ImageField(upload_to=image_upload_path)

    # crud = models.ForeignKey('Product', on_delete=models.CASCADE)
    def __int__(self):
        return self.tag_image

    class Meta:
        db_table = 'tag'