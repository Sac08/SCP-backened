from __future__ import print_function
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions

from .models import MockSchedular
from .serializers import *

from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

#connecting to Google
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import os

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def students_list(request):
    if request.method == 'GET':
        data = MockSchedular.objects.all()

        serializer = StudentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([permissions.AllowAny])
def students_detail(request, pk):
    try:
        student = MockSchedular.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
    elif request.method == 'GET':
        data = MockSchedular.objects.filter(pk = pk)

        serializer = StudentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sendmail(request, pk):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    a = os.path.dirname(__file__)
    store = file.Storage(a + '/storage.json')
    print(store)
    creds = store.get()
    flags = tools.argparser.parse_args([])
    if not creds or creds.invalid:
        #data = open(a+'/client_secrets.json', 'rb')
        #print(data)
        flow = client.flow_from_clientsecrets(a+'/client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store,flags)
    GCAL = build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '+05:30'      # PDT/MST/GMT-7
    EVENT = {
        'summary': 'Mock Interview - IIITB',
        'start':  {'dateTime': request.data["date"] + 'T' + request.data["time"] + '%s' % GMT_OFF},
        'end':    {'dateTime': request.data["date"] + 'T' + request.data["time"] + '%s' % GMT_OFF},
        'attendees': [
            {'email': request.data["email"]},
            {'email': request.data["email1"]},
        ],
    }

    e = GCAL.events().insert(calendarId='primary',
            sendNotifications=True, body=EVENT).execute()
    print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'], e['end']['dateTime']))
    '''
    subject = 'MockInterviewIIITB'
    message = 'Congratulations! ' + '\n' + request.data["name"] + ' and ' + request.data["name1"] + ' have MockInterview' + ' at ' + request.data["time"] + ', ' + request.data["date"] + " on " + request.data["topic"] + '\nthis is your link ' + 'https://hangouts.google.com/call/ftwkBvHA27fM028mYImMAAEM' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.data["email"],request.data["email1"],]
    send_mail( subject, message, email_from, recipient_list )
    '''
    return Response(status=status.HTTP_201_CREATED)
