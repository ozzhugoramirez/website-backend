from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class HelloWord(APIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
   


