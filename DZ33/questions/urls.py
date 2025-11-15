from django.urls import path
from django.urls import include
from questions.views import question,hot_questions,settings,tag,ask,login,signup
from . import views

urlpatterns = [
    path('hot/', hot_questions, name='hot_questions'),
    path('<int:id>/', question, name='question'),
    path('settings/', settings, name='settings'),
    path('tag/<str:tag_name>/', tag, name='tag'), 
    path('ask/', ask, name='ask'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    
]