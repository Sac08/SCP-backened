from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from SCPapp import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getData/', views.getData.as_view()),
    path('postData/', views.postData.as_view()),
    path('deleteData/<id>', views.deleteData)
       
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)