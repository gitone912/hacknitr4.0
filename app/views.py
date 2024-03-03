from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from .bot import call_bot
from django.http import JsonResponse
from .models import *
from .intent_ana import *
from .gpt import *
from .llama import *
#import csrf extempt
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment
from .whisperapp import *
from .forms import AudioFileForm
from app.langchain_bot import *
# Create your views here.

chat_chain = create_chat_chain(api_key, system_prompt)
def homepage(request):
    return render(request, 'Homepage.html')
@csrf_exempt
def bot(request):
    if request.method == 'POST':
        try:
            user_input = request.POST.get('user_input', '')
            response = chat(chat_chain, user_input)
            print(response)
            # Save the chat history
            Chat.objects.create(user_input=user_input, response=response)
            print("created")
            chat_history = Chat.objects.all().order_by('-timestamp')
            return render(request, 'bot.html', {'chat_history': chat_history})
        except Exception as e:
            print(e)
            print("error")
            return render(request, 'bot.html', {'error': str(e)})

    # Retrieve all chat history
    chat_history = Chat.objects.all().order_by('-timestamp')
    return render(request, 'bot.html', {'chat_history': chat_history})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('survey')  
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'login.html', {'error_message': error_message})

def signup_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different one.'
        elif User.objects.filter(email=email).exists():
            error_message = 'Email already exists. Please use a different one.'
        else:
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('login')  

    return render(request, 'signup.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

def analyse_intent(request):
    if request.method == 'POST':
        try:
            # Get the user input from the request data
            user_input = request.POST.get('user_input', '')
            response = main_function(user_input)
            
            return render(request, 'intent.html',{'response': response})
        except Exception as e:
            return render(request, 'intent.html', {'error': str(e)})
    return render(request, 'intent.html')


def music(request):
    return redirect('http://127.0.0.1:8001')


def playlist(request):
    return render(request, 'playlist.html')

def dashboard(request):
    return render(request,'index.html')

def avatar(request):
    return render(request,'avatar.html')

def task(request):
    return render(request,'Tasks.html')

def survey(request):
    return render(request,'survey.html')


from os.path import join, dirname
from dotenv import load_dotenv
import vonage


def notification(request):
    if request.method == 'POST':
        number = request.POST.get('user_input', '') 
        dotenv_path = join(dirname(__file__), "../.env")
        load_dotenv(dotenv_path)

        VONAGE_API_KEY = "e8e6fb61"
        VONAGE_API_SECRET = "7NCsDAIv5fAUFjLV"
        VONAGE_BRAND_NAME = "akash"
        TO_NUMBER = f'{number}'


        client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

        responseData = client.sms.send_message(
            {
                "from": VONAGE_BRAND_NAME,
                "to": TO_NUMBER,
                "text": "Hello Dear Hope you doing fine, Wanna Chat a little bit?",
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
            return redirect('dashboard')
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            return redirect('dashboard')
    else:
        return render(request,'notification.html')


def congrats(request):
    return render(request,'congrats.html')


def dynamic_tasks(request):
    user_input = "generate 10 tasks for me to cure my mental health in a list form separated by commas"
    response = run_chatbot(user_input)
            
    return render(request, 'dynamic_tasks.html',{'response': response})

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import requests
import os

API_KEY = "cd86c2677cef4a878100c664dc169772"
ENDPOINT = "https://ic2024emotiondetection.cognitiveservices.azure.com/"

@csrf_exempt
def camera(request):
    return render(request, 'cmera.html')

@csrf_exempt
def capture_and_analyze(request):
    if request.method == 'POST':
        # Assuming the input field name is 'image'
        image_file = request.FILES.get('image')

        if image_file:
            captured_image = CapturedImage.objects.create(image=image_file)

        result = analyze_image(f'/Users/pranaymishra/Desktop/backend_MinMin/backend/{captured_image.image.url}')
        print(result)

        Results.objects.create(result=result)
        return redirect('result')
    else:
        return render(request, 'cmera.html')

def latest_result(request):
    latest_object = Results.objects.latest('timestamp')
    context = {'latest_result': latest_object}
    return render(request, 'result.html', context)
    
def analyze_image(image_path):
    print("capturing")
    subscription_key = API_KEY
    endpoint = ENDPOINT

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    with open(image_path, 'rb') as image_file:
        # Call API with local image
        tags_result = computervision_client.tag_image_in_stream(image_file)

        # Process the result and return relevant information
        tags = [{'name': tag.name, 'confidence': tag.confidence * 100} for tag in tags_result.tags]
        return tags





def process_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    processed_audio = audio.export(file_path.replace('.wav', '.mp3'), format='mp3')
    return processed_audio

def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            file_path = audio_file.audio.path
            processed_audio = process_audio(file_path)
            audio_file.audio.name = audio_file.audio.name.replace('.wav', '.mp3')
            audio_file.audio.save(audio_file.audio.name, processed_audio)
            result = transcribe_mp3(file_path.replace('.wav', '.mp3'))
            print(result)
            return render(request, 'sucess.html', {'result': result})
    else:
        form = AudioFileForm()
    return render(request, 'upload_audio.html', {'form': form})


from .forms import AudioRecordingForm

@csrf_exempt
def record_audio(request):
    if request.method == 'POST':
        form = AudioRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            return JsonResponse({'status': 'success', 'audio_url': audio_file.audio_file.url})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = AudioRecordingForm()

    return render(request, 'record_audio.html', {'form': form})


def get_latest_audio_recording_path():
    try:
        # Get the latest audio recording file
        latest_recording = AudioRecording.objects.latest('id')
        return latest_recording.audio_file.path
    except AudioRecording.DoesNotExist:
        print("No audio recordings found.")
        return None

def transcribe_latest_audio_recording(request):
    # Get the latest audio recording file path
    latest_audio_path = get_latest_audio_recording_path()

    if latest_audio_path:
        # Transcribe the latest audio recording
        transcription = transcribe_mp3(latest_audio_path)
        print(transcription)
        response = chat(chat_chain, transcription)
        return JsonResponse({'status': 'success', 'transcription': response})
    else:
        # Handle the case when no audio recording is found
        return JsonResponse({'status': 'error', 'message': 'No audio recording found'})
    
def final(request):
    return render(request,'twourls.html')