from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('', FilewithId.as_view())
]