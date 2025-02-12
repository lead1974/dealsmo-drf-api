from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class CustomUserDetailsView(APIView):
    def get(self, request):
        # Your logic here
        return Response({"message": "User details"})
