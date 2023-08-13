from rest_framework import serializers
from .models import Product, Clothes
from tag.models import Tag


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    # 게시글에 등록된 태그 가져오기
    def get_images(self, obj):
        image = obj.tag.all()

    class Meta:
        model = Product
        fields =  "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductInsertSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'user', 'description', 'filename', 'modify_dt', 'tag', 'images']

    def create(self, validated_data):
        # product_code = validated_data.get('product_code')
        #product_name = validated_data.get('product_name')
        #user = validated_data.get('user')
        #description = validated_data.get('description')
        #filename = validated_data.get('filename')
        tags_data = validated_data.pop('tag', [])
        product = Product.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(tag_name = tag_data.tag_name)
            product.tag.add(tag)
        return product
        #product = Product(
        #    product_name = product_name,
        #    user = user,
        #    description = description,
        #    filename = filename,
        #    tag = tag,
        #)
        #product.save()
        #return Product

class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        field = "__all__"
"""
class TagSerializer(serializers.ModelSerializer): #
    class Meta:
        model = Tag
        field = "__all__"
"""