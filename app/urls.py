from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("bot/", bot, name="bot"),
    path("intent_analysis/", analyse_intent, name="intent_analysis"),
    path('dashboard/',dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('',homepage, name='login'),
    path('playlist/',playlist, name='playlist'),
    path('avatar/',avatar, name='avatar'),
    path('task/',task, name='task'),
    path('survey/',survey, name='survey'),
    path('notification/',notification, name='notification'),
    path('congrats/',congrats, name='congrats'),
    path("dynamic_task/", dynamic_tasks, name="dynamic_task"),
    path('capture_and_analyze/', capture_and_analyze, name='capture_and_analyze'),
    path('camera/', camera, name='camera'),
    path('results/',latest_result,name='result'),
    path('music/',music,name='music'),
    # path('upload/', upload_audio, name='upload'),
    path('audio/', record_audio, name='avatar'),
    path('transcribe/',transcribe_latest_audio_recording, name='transcribe'),
    path('final',final,name='final')

    
]
