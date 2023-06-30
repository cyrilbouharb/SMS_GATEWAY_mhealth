from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from twilio.rest import Client as TwilioClient
import difflib
import os
from .models import PhoneNumber
import re
from dotenv import find_dotenv, load_dotenv

def input(request):
    numbers = PhoneNumber.objects
    return render(request, 'smsgateaway/base2.html', {'phonenumbers':numbers})

@login_required(login_url="/accounts/login")
def sms_gateway_view(request):
    if request.method == 'POST':
        raw_phone_number = request.POST.get('phone_number')
        phone_number = sanitize_phone_number(raw_phone_number)
        if not phone_number.isdigit():
            messages.error(request, 'Invalid phone number. Please enter a valid phone number.')
            return render(request, 'smsgateaway/input.html')
        carrier_name = look_up_carrier(phone_number)
        matching_carriers = match_carrier(carrier_name, phone_number)
        return render(request, 'smsgateaway/result.html', {'matching_carriers': matching_carriers})
    return render(request, 'smsgateaway/input.html')

def sanitize_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if not phone_number or len(phone_number)<10:
        return ''
    return phone_number


def look_up_carrier(phone_number, country='US'):
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    SID = os.getenv("SID")
    TOKEN = os.getenv("TOKEN")
    client = TwilioClient(SID, TOKEN)

    phone_data = client.lookups.v1.phone_numbers(phone_number).fetch(country_code=country, type=['carrier'])

    return phone_data.carrier['name']

def match_carrier(carrier, phone_number):
    carriers = get_clean_carrier_list(phone_number)

    close_matches = [c for c in carriers if carrier.split(" ")[0] in c]

    if len(close_matches) == 0:
        close_matches = difflib.get_close_matches(carrier, list(carriers))

    print(f"Closest matches to '{carrier}': {close_matches}")

    matching_carriers = {}

    for c in close_matches:
        matching_carriers[c] = carriers[c]

    return matching_carriers


def get_clean_carrier_list(phone_number):
    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(current_path, 'data')
    carriers_file = os.path.join(data_dir, 'carriers.txt')

    with open(carriers_file, 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines if len(l) > 2]

    carriers = {}

    for line in lines:
        if "@" not in line:
            carrier = line
            carriers[carrier] = []
        else:
            email= line.split("@")[1]
            format = phone_number + "@" + email
            carriers[carrier].append(format)

    return carriers


@login_required(login_url="/accounts/login")
def result_view(request):
    matching_carriers = request.GET.get('matching_carriers')
    return render(request, 'smsgateaway/result.html', {'matching_carriers': matching_carriers})
