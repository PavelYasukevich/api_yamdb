from django.shortcuts import render
from django.shortcuts import get_object_or_404 
from rest_framework.viewsets import ModelViewSet 
 
from .models import Title, Review, User
from .serializers import (ReviewSerializer, CommentSerializer) 

# Create your views here.

class ReviewViewSet(ModelViewSet): 
    serializer_class = ReviewSerializer 
 
    def get_queryset(self): 
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        queryset = Review.objects.filter(title_id=title) 
        return queryset 
 
    def perform_create(self, serializer): 
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        return serializer.save(author=self.request.user, title_id=title) 


class CommentViewSet(ModelViewSet): 
    serializer_class = CommentSerializer
 
    def get_queryset(self): 
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        queryset = Comment.objects.filter(title_id=title) 
        return queryset 
 
    def perform_create(self, serializer): 
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        return serializer.save(author=self.request.user, title_id=title)
