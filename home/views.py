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
        esp32_ip = 'http://172.20.10.14/receive-message'  # Replace with the actual IP address and endpoint

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

def custom_admin_index(request):
    return render(request, 'home/templates/admin/index.html')

def custom_admin_lock_dashboard(request):
    return render(request, 'home/templates/admin/lock_dashboard.html')

def get_gps_data(request):
    esp32_ip = 'http://172.20.10.14/get-gps-data'  # Replace with the actual IP address and endpoint of your ESP32

    try:
        # Send a GET request to the ESP32 to fetch GPS data
        response = requests.get(esp32_ip)
        if response.status_code == 200:
            return JsonResponse(response.json())  # Assuming the ESP32 returns a JSON response
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch GPS data from ESP32.'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
