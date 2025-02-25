from django.http import HttpResponse
from currency import forms
from django.shortcuts import render
import requests
import json

def convert_currency(request):
    
    # Calling API using requests lib
    api_request = requests.get("http://data.fixer.io/api/latest?access_key=40eac7a32ba84e0369830d99248246b7")
    
    if api_request.status_code == 200:
        currency_dict = api_request.json()
        currency_rates_dict = currency_dict['rates']
        list_of_country_currency_code = currency_rates_dict.keys()
        tuple_of_country_codes = [(x, x) for x in list_of_country_currency_code]
        
        # Initialize form with country currency code
        currency_form = forms.CurrencyForm(tuple_of_country_codes, request.POST or None)
        converted_currency = ""
        
        if request.method == "POST":
            # Check sanitation
            if currency_form.is_valid():
                # Values from the HTML input fields
                source_currency_code = currency_form.cleaned_data['source_currency_code']
                target_currency_code = currency_form.cleaned_data['target_currency_code']
                input_currency_value = currency_form.cleaned_data['source_currency_value']
                
                # Get live amount of selected country 
                from_country_base_value = currency_rates_dict[source_currency_code]
                to_country_base_value = currency_rates_dict[target_currency_code]
                
                # Logic to calculate the converted currency
                converted_currency = (to_country_base_value / from_country_base_value) * float(input_currency_value)
                
                return render(request, 'currency/currency-index.html', {
                    'currency_form': currency_form, 
                    'converted_currency': converted_currency
                })
        
        # Form initialization
        context = {
            'currency_form': currency_form,
            'converted_currency': converted_currency
        }
        return render(request, 'currency/currency-index.html', context)
    
    else:
        return HttpResponse("Error fetching data from the currency API", status=500)
