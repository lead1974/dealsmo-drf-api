from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .permissions import ProductPermission
from .serializers import ProductSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def perform_create(self, serializer):
        # Set the current user as author
        product = serializer.save()
        product._current_user = self.request.user
        product.save()
