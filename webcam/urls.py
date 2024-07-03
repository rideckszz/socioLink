from django.urls import path
from . import views
from .views import escreve_ai
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('escreveAI/', escreve_ai, name='escreveAI'),
    path('emocionAI/', views.emocionAI, name='emocionAI'),
    path('sobre/', views.sobre, name='sobre'),
    path('referencias/', views.referencias, name='referencias'),
    path('detect/', views.detect_emotion, name='detect_emotion'), 
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
