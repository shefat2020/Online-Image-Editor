from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getImage/', views.getImage, name='getImage'),
    path('canvas/', views.canvas, name='canvas'),
    path('save/', views.save, name='save'),
    path('undo/', views.undo, name='undo'),

    path('gray/', views.gray, name='gray'),
    path('rotate_left/', views.rotate_left, name='rotate_left'),
    path('rotate_right/', views.rotate_right, name='rotate_right'),
    path('detect_edge/', views.detect_edge, name='detect_edge'),
    path('meanfilter/', views.meanfilter, name='meanfilter'),
    path('midpoint_filter/', views.midpoint_filter, name='midpoint_filter'),
    path('negative/', views.negative, name='negative'),
    path('add_bright', views.add_bright, name='add_bright'),
    path('remove_bright', views.remove_bright, name='remove_bright'),
    path('GaussianBlur', views.GaussianBlur, name='GaussianBlur'),
    path('medianBlur', views.medianBlur, name='medianBlur'),
    path('crop_left', views.crop_left, name='crop_left'),
    path('crop_right', views.crop_right, name='crop_right'),
    path('crop_up', views.crop_up, name='crop_up'),
    path('crop_down', views.crop_down, name='crop_down'),
    path('canvas/resize', views.resize, name='resize'),
]