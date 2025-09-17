from rest_framework import serializers
from .models import *


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id','product','image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'description']


class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)  # 🔑 related_name="images" orqali
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'brand','price','discount_percentage','discount_price','image','category','images']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','product','created_at']


class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ['id','about','image']



class AboutSerializer(serializers.ModelSerializer):
    images = AboutImageSerializer(many=True, read_only=True)
    class Meta:
        model = About
        fields = ['id','title','description','image','images']

class AnnouncementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementImage
        fields = ['id', 'announcement','image']


class AnnouncementSerializer(serializers.ModelSerializer):
    images = AnnouncementImageSerializer(many=True, read_only=True)
    class Meta:
        model = Announcement
        fields = ['id','title','description','image','images']