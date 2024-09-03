from django.shortcuts import render
from django.http import HttpResponse

import requests
from django.conf import settings
from django.http import JsonResponse
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

def index(request):
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
    

@csrf_exempt  # This decorator exempts this view from CSRF verification.
def set_locked(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            locked_state = data.get('locked', False)  # Default to False if not provided

            # Prepare the ESP32 endpoint URL
            esp32_ip = 'http://172.20.10.14/set-lock-state'  # Replace with your actual ESP32 endpoint

            # Send a request to ESP32 with the lock state
            response = requests.post(esp32_ip, json={'locked': locked_state})
            
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Lock state updated successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to update lock state on ESP32.'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

## 0904 add https
@csrf_exempt  # Use this decorator to allow POST requests without a CSRF token for this view
def receive_gps_data(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            device_id = data.get('deviceID')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            altitude = data.get('altitude')
            speed = data.get('speed')
            satellites = data.get('satellites')
            
            # Your logic to verify the device ID and handle the GPS data
            valid_device_ids = ["goodlock2u", "goodlock4u"]
            if device_id in valid_device_ids:
                # Device ID is valid
                return JsonResponse({'status': 'success', 'message': 'Device ID is valid'})
            else:
                # Device ID is invalid
                return JsonResponse({'status': 'failure', 'message': 'Invalid Device ID'})
                
        except json.JSONDecodeError:
            # Handle JSON parsing error
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        # Handle invalid HTTP method
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
## 0904 add https