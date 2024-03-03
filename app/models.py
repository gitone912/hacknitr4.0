from django.db import models

class Chat(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
class CapturedImage(models.Model):
    image = models.ImageField(upload_to='captured_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Results(models.Model):
    result = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
from django.db import models

class AudioFile(models.Model):
    audio = models.FileField(upload_to='audio/')
    
class AudioRecording(models.Model):
    audio_file = models.FileField(upload_to='audio_recordings/')