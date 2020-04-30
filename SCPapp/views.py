from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import File
from .serializers import serializers
from django.shortcuts import render, redirect

from .serializers import FileSerializer

class getData(APIView):

    def get(self, request, *args, **kwargs):
        allFiles = File.objects.all()
        for key in request.data.keys():
            value = request.data.get(key)
            if (key == 'resourceType'):
                allFiles = allFiles.filter(resourceType=value)
            elif (key == 'semester'):
                allFiles = allFiles.filter(semester=value)
            elif (key == 'subject'):
                allFiles = allFiles.filter(subject=value)
            elif (key == 'year'):
                allFiles = allFiles.filter(year=value)
            elif (key == 'id'):
                allFiles = allFiles.filter(id=value)
        
        serializer = FileSerializer(allFiles, many=True)
        return Response(serializer.data)

class postData(APIView):

    def post(self, request, *args, **kwargs):        
        file_serializer = FileSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def deleteData(request, id):
    try:
        field = File.objects.get(id = id)
    except File.DoesNotExist:
        return redirect('/getData')
    field.delete()
    return redirect('/getData')