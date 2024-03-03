from django import forms
from .models import AudioFile ,AudioRecording

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audio']

class AudioRecordingForm(forms.ModelForm):
    class Meta:
        model = AudioRecording
        fields = ['audio_file']