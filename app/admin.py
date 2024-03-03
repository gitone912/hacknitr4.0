from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Chat)
admin.site.register(CapturedImage)
admin.site.register(Results)
admin.site.register(AudioFile)
admin.site.register(AudioRecording)