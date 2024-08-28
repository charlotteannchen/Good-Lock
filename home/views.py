from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import requests
from django.conf import settings
from django.http import JsonResponse
import urllib.parse

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')


def lock_dashboard(request):
    return render(request, 'pages/lock_dashboard.html')

def send_message_to_esp32(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        esp32_ip = 'http://10.0.175.67/receive-message'  # Replace with the actual IP address and endpoint

        try:
            # Send the message to the ESP32
            response = requests.post(esp32_ip, data={'message': message})
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to send message to ESP32.'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})