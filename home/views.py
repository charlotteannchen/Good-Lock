from django.shortcuts import render
from django.http import HttpResponse

import requests
from django.conf import settings
from django.http import JsonResponse
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

ESP32_IP = 'http://172.20.10.14'
def index(request):
    return render(request, 'pages/index.html')

def lock_dashboard(request):
    return render(request, 'pages/lock_dashboard.html')

def send_message_to_esp32(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        try:
            # Send the message to the ESP32
            response = requests.post(f'{ESP32_IP}/receive-message', data={'message': message})
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

    try:
        response = requests.get(f'{ESP32_IP}/get-gps-data')
        if response.status_code == 200:
            return JsonResponse(response.json())  # Assuming the ESP32 returns a JSON response
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch GPS data from ESP32.'})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt  # Temporarily disable CSRF protection for testing purposes
def receive_device_id(request):
    if request.method == 'POST':
        device_id = request.POST.get('id')
        # Process the device ID (e.g., save to the database)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt  # This decorator exempts this view from CSRF verification.
def set_locked(request):
    if request.method == 'POST':
        try:
            print("body", request.body)
            data = json.loads(request.body)
            locked_state = data.get('locked', False)  # Default to False if not provided
            
            json_data = '{"locked":' + ('true' if locked_state else 'false') + '}'
            
            headers = {'Content-Type': 'application/json'}
            print("json_data", json_data)
            response = requests.post(f'{ESP32_IP}/set_locked', data=json_data, headers=headers)
            print("====", response.text)
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Lock state updated successfully.'})
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to update lock state on ESP32.',
                    'details': response.text  # Add the response text from the ESP32 for more info
                })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})