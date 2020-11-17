from django.db import models 
from rest_framework import serializers 
 
from .models import Title, Review, User, Comment


class ReviewSerializer(serializers.ModelSerializer): 
    author = serializers.StringRelatedField() 
 
    class Meta: 
        fields = ('id','title_id', 'author', 'text', 'score', 'pub_date') 
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    class Meta:
        fields = ('id','review_id', 'author', 'text', 'pub_date')
        model = Comment