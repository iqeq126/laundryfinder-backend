from django.db import models

# Create your models here.


class Image(models.Model):
    language = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    translate = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.language, self.translate
