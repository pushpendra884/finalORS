from django.urls import path
from .import views

urlpatterns=[
    path('',views.index),
    # path("<page>/<action>",views.action),
    path("<page>/",views.actionId),
    path("<page>/<operation>/<int:id>",views.actionId),
    path('auth/<page>/', views.auth),
  
]