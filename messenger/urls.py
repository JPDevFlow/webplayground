from django.urls import path
from .views import ThreadList, ThreadDetail


messenger_patterns = ([
    path('', ThreadList.as_view(), name='thread_list'),
    path('thread/<int:pk>/', ThreadDetail.as_view(), name='detail'),
], "messenger")