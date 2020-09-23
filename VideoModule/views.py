from django.shortcuts import render
from django.http import Http404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import VideoContent, Comments
from .serializers import serializers
from SCPapp.models import User
from SCPapp.serializers import UserSerializer
from rest_framework.decorators import api_view

from .serializers import VideoContentSerializer, CommentsSerializer

class postData(APIView):
    def post(self, request, *args, **kwargs):        
        videoContentSerializer = VideoContentSerializer(data=request.data)
        
        if videoContentSerializer.is_valid():
            videoContentSerializer.save()
            return Response(videoContentSerializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(videoContentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class getData(APIView):
    def get(self, request, *args, **kwargs):
        allVideoFiles = VideoContent.objects.filter(verified=True)

        for key in request.GET.keys():
            value = request.GET.get(key)
                        
            if (key == 'semester'):
                allVideoFiles = allVideoFiles.filter(semester=value)
            elif (key == 'subject'):
                allVideoFiles = allVideoFiles.filter(subject=value)
            elif (key == 'year'):
                allVideoFiles = allVideoFiles.filter(year=value)
            elif (key == 'speaker'):
                allVideoFiles = allVideoFiles.filter(speaker__icontains=value)
            elif (key == 'id'):
                allVideoFiles = allVideoFiles.filter(id=value)
        
        serializer = VideoContentSerializer(allVideoFiles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def videoAdminView(request):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')
        if (role=='admin'):
            product1 = VideoContent.objects.filter(verified=False)
            serializer = VideoContentSerializer(product1, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class getDataById(APIView):
    def get_object(self, id):
        try:
            return VideoContent.objects.get(id=id)
        except VideoContent.DoesNotExist:
            raise Http404

    def get(self, request, id):
        user=User.objects.get(rollNumber=request.user)
        user_serializer = UserSerializer(user)

        role=user_serializer.data.get('role')
        allVideoFiles = self.get_object(id)
        serializer = VideoContentSerializer(allVideoFiles)
        verified=serializer.data.get('verified')
        # not returning anything if the page is not verified and user is a student
        if ((role == 'Student') and (verified == False)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data)

class updateData(APIView):
    def get_object(self, id):
        try:
            return VideoContent.objects.get(id=id)
        except VideoContent.DoesNotExist:
            raise Http404
    
    def patch(self, request, id):
        Video = self.get_object(id)
        serializer = VideoContentSerializer(Video, data=request.data, partial=True)

        if (serializer.is_valid()):
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteData(APIView):
    def get_object(self, id):
        try:
            return VideoContent.objects.get(id=id)
        except VideoContent.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        Video = self.get_object(id)
        Video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class getPostComments(APIView):
    def get(self, request, id):
        allComments = Comments.objects.all().filter(videocontent=id)

        commentsSerializer = CommentsSerializer(allComments, many=True)
        return Response(commentsSerializer.data)

    def post(self, request, id):
        user=User.objects.get(rollNumber=request.user)
        serializer = UserSerializer(user)
        name=serializer.data.get('rollNumber')+"_"+serializer.data.get('username')
        request.data['author']=name
        
        commentsSerializer = CommentsSerializer(data=request.data)
        
        if commentsSerializer.is_valid():
            commentsSerializer.save()
            return Response(commentsSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(commentsSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_comment(self, id):
        try:
            return Comments.objects.get(id=id)
        except Comments.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        Comment = self.get_comment(id)
        Comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)