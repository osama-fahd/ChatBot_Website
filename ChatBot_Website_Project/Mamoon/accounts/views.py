from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def sign_up(request: HttpRequest):
    if request.method == "POST":

        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request, "You'r Registered Successfuly!", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            print(e)

    return render(request, "accounts/signup.html")

# In accounts/views.py

def create_rocketchat_contact(user: User):
    """
    Searches for a Rocket.Chat contact by email and creates one if it doesn't exist,
    including the Django username as a custom field.
    """
    if not hasattr(settings, 'ROCKETCHAT_API_URL'):
        print("Rocket.Chat settings not configured in Django.")
        return

    # (The search logic remains the same...)
    search_url = f"{settings.ROCKETCHAT_API_URL}/api/v1/omnichannel/contact.search"
    headers = {
        'X-Auth-Token': settings.ROCKETCHAT_AUTH_TOKEN,
        'X-User-Id': settings.ROCKETCHAT_USER_ID,
    }
    
    try:
        search_params = {'email': user.email}
        response = requests.get(search_url, headers=headers, params=search_params)
        response.raise_for_status()
        search_result = response.json()
        
        if not search_result.get('contact'):
            print(f"Contact for {user.email} not found. Creating...")
            create_url = f"{settings.ROCKETCHAT_API_URL}/api/v1/omnichannel/contacts"
            
            payload = {
                "name": f"{user.first_name} {user.last_name}",
                "emails": [user.email],
                # >> ADD THE CUSTOM FIELD DATA HERE <<
                "customFields": {
                    "djangoUsername": user.username
                }
            }
            
            create_response = requests.post(create_url, headers=headers, json=payload)
            create_response.raise_for_status()
            print(f"Successfully created Rocket.Chat contact for {user.email}")
        else:
            print(f"Rocket.Chat contact for {user.email} already exists.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not create Rocket.Chat contact for {user.email}. Reason: {e}")



def sign_in(request:HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request, user)
            messages.success(request, "You'r Logged In Successfully!", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again", "alert-danger")

    return render(request, "accounts/signin.html")



def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "You'r Logged Out Successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))
