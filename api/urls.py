from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('callback/', views.callback, name='callback'),
    path('analisarPlaylist/', views.analisarPlaylist, name='analisarPlaylist')
]
