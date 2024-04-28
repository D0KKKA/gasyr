
from django.urls import path
from .views import *

urlpatterns = [
    #path('start/', StartConvoView.as_view(), name='start_convo'),
    path('<int:pk>/', GetConversationView.as_view(), name='get_conversation'),

]