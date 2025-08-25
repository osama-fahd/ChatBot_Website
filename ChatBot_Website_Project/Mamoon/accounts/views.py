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
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST["email"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"]
            )
            # .create_user() already saves, so new_user.save() is not needed.

            # >> ADD THIS LINE TO CALL YOUR FUNCTION <<
            create_rocketchat_contact(new_user)

            messages.success(request, "You'r Registered Successfuly!", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            print(e)
            messages.error(request, "Registration failed. The username may already exist.", "alert-danger")

    return render(request, "accounts/signup.html")

# in accounts/views.py

def create_rocketchat_contact(user: User):
    """
    Searches for a Rocket.Chat contact by the custom field 'djangoUsername'
    and creates one if it doesn't exist.
    """
    if not hasattr(settings, 'ROCKETCHAT_API_URL'):
        print("Rocket.Chat settings not configured in Django.")
        return

    search_url = f"{settings.ROCKETCHAT_API_URL}/api/v1/omnichannel/contact.search"
    headers = {
        'X-Auth-Token': settings.ROCKETCHAT_AUTH_TOKEN,
        'X-User-Id': settings.ROCKETCHAT_USER_ID,
    }
    
    try:
        search_params = {'custom': f'{{"djangoUsername": "{user.username}"}}'}
        response = requests.get(search_url, headers=headers, params=search_params)
        response.raise_for_status()
        search_result = response.json()

        # >> NEW LOGIC TO VERIFY EXACT MATCH <<
        contact_exists_exactly = False
        if search_result.get('contact'):
            # The API found a partial match, now we check it precisely.
            # Note: The API might return a single object or a list. This handles both.
            contacts = search_result['contact']
            if not isinstance(contacts, list):
                contacts = [contacts]
            
            for contact in contacts:
                custom_fields = contact.get('customFields', {})
                if custom_fields.get('djangoUsername') == user.username:
                    contact_exists_exactly = True
                    break # Found an exact match, no need to check further

        # Now, create the contact only if no exact match was found
        if not contact_exists_exactly:
            print(f"Contact for {user.username} not found with an exact match. Creating...")
            create_url = f"{settings.ROCKETCHAT_API_URL}/api/v1/omnichannel/contacts"
            
            payload = {
                "name": user.first_name,
                "emails": [user.email],
                "phones": [user.username],
                "customFields": {
                    "djangoUsername": user.username
                }
            }
            
            create_response = requests.post(create_url, headers=headers, json=payload)
            create_response.raise_for_status()
            print(f"Successfully created Rocket.Chat contact for {user.username}")
        else:
            print(f"Rocket.Chat contact for {user.username} already exists.")

    except requests.exceptions.RequestException as e:
        # >> THIS MODIFIED BLOCK GIVES US DETAILED ERRORS <<
        error_message = f"ERROR: Could not process Rocket.Chat contact for {user.username}."
        if e.response is not None:
            # This will print the specific JSON error from Rocket.Chat
            error_message += f" Reason: {e.response.json()}"
        else:
            error_message += f" Reason: {e}"
        print(error_message)



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
