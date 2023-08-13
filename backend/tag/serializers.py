from rest_framework import serializers
from .models import Tag
"""
class TagImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = TagImage
        fields = ['id','tag', 'image']
"""

class TagSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    #게시글에 등록된 이미지들 가지고 오기
    """
    def get_images(self, obj):
        image = obj.image.all()
        return TagImageSerializer(instance=image, many=True, context=self.context).data
    """
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        instance = Tag.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('tag_image'):
            Tag.objects.create(post=instance, image=image_data)
        return instance
"""
class TagSerializer(serializers.ModelSerializer): #
    class Meta:
        model = Tag
        field = ["tag_name"]
"""