from django.shortcuts import render
import requests
import pandas as pd
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
import csv

def index(request):
    return render(request, "index.html",)

def consultation(request):
    if request.method == 'POST':
        location = request.POST.get('location', '')  
        doctors = get_doctors_by_location(location) 
        print("Doctors:", doctors)
        print("Location:", location)
        return render(request, 'consultation.html', {'doctors': doctors, 'location': location})
    else:
        return render(request, 'consultation.html')  

def get_doctors_by_location(location):
    """Reads doctor data from CSV and returns a list of doctors for the given location."""
    doctors = []
    try:
        with open('data/doctors.csv', 'r') as csvfile: 
            reader = csv.DictReader(csvfile)
            for row in reader:
                if location.lower() in row['Location'].lower():  
                    doctors.append(row)
    except FileNotFoundError:
        print("doctors.csv not found")
        return [] 

    return doctors
        

def medinav(request):
    prices = []
    medication_name = ""

    if request.method == "POST":
        medication_name = request.POST.get("medication_name")
        print("Medication Name:", medication_name)
        prices = get_medication_prices_csv(medication_name)
        print("Prices:", prices)

   
    
    return render(request, 'medinav.html', context={'medication_name': medication_name, 'prices': prices})


def get_medication_prices_csv(medication_name):
    """Fetches medication prices from a CSV file."""
    try:
        df = pd.read_csv("data/md.csv") 
        filtered_df = df[df["Name"].str.contains(medication_name, case=False)]

        prices = []
        for index, row in filtered_df.iterrows():
            pharmacy = row["Pharmacy"]
            price = row["Price"]
            cc= row["coupon_code"]
            dosage=row["Dosage"]
            quantity=row["Quantity"]
            location=row["Location"]
            prices.append({"pharmacy": pharmacy, "price": price, "coupon_code": cc, "dosage": dosage, "quantity": quantity, "location": location})
        return prices
    
    except FileNotFoundError:
        print("Error: medication_data.csv not found.")
        return []
    

    
def get_ai_response(message):
    
     if "medicine" in message.lower():
         return "I can help you find information about medications."
     elif "consultation" in message.lower():
         return "You can book a consultation on our website."
     else:
         return "I'm here to assist you with medical information. How can I help?"

@csrf_exempt  
def ai_response_view(request):
     if request.method == 'POST':
         try:
             data = json.loads(request.body) 
             message = data['message']
             response = get_ai_response(message)
             return JsonResponse({'response': response})
         except json.JSONDecodeError:
             return JsonResponse({'error': 'Invalid JSON'}, status=400)
     else:
         return JsonResponse({'error': 'Method not allowed'}, status=405)


