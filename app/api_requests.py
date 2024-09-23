from dotenv import load_dotenv
import os
import random
import requests
from flask import jsonify
from datetime import datetime, timedelta

load_dotenv()
api_token = os.getenv('API_TOKEN')


def check_availability():

    start_date = datetime.now().isoformat() + 'Z'
    end_date = datetime.now() + timedelta(days=5)
    end_date_formatted = end_date.isoformat() + 'Z' 
    print(start_date)
    print(end_date)

    url = "https://api.xandar.instaleap.io/jobs/availability/v2"

    payload = {
        "origin": {
            "name": "Origin P1",
            "address": "Cra. 100 23h-2 a 23h-100, Bogotá, Colômbia",
            "latitude": 4.68062,
            "longitude": -74.135074
        },
        "destination": {
            "name": "Destination P1",
            "address": "Cl. 69, Bogotá, Colômbia",
            "latitude": 4.69882,
            "longitude": -74.119155
        },
        "currency_code": "COP",
        "start": start_date,
        "end": end_date_formatted,
        "slot_size": 15,
        "operational_models_priority": ["FULL_SERVICE"],
        "fallback": True,
        "store_reference": "101_FS",
        "job_items": [
            {
                "id": "string",
                "name": "string",
                "unit": "g",
                "sub_unit": "g",
                "quantity": 1,
                "sub_quantity": 1,
                "price": 10
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_token
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_job(slot_id):

    new_client_reference = f"client - {random.randint(1, 5000)}"
    print(new_client_reference)

    url = "https://api.xandar.instaleap.io/jobs"

    payload = {
        "recipient": {
            "name": "string2",
            "email": "test@gmail.com",
            "phone_number": "+52 22342342"
        },
        "payment_info": {
            "prices": {
                "order_value": 10,
                "attributes": [
                    {
                        "type": "ORDER_VALUE",
                        "name": "string",
                        "value": 10
                    }
                ]
            },
            "payment": {
                "method": "CASH",
                "metadata": { "newKey": "New Value" },
                "payment_status": "SUCCEEDED",
                "value": 10,
                "blocking_policy": "CHECKOUT",
                "id": "string",
                "payment_status_details": "string",
                "method_details": "string"
            },
            "currency_code": "COP"
        },
        "add_delivery_code": True,
        "contact_less": {
            "comment": "LeaveAtTheDoor",
            "cash_receiver": "string2",
            "phone_number": "+52 22342342"
        },
        "slot_id": slot_id,
        "client_reference": new_client_reference
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_token
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()

def display_orders_details(order_id):
    url = f"https://api.xandar.instaleap.io/jobs/{order_id}"

    headers = {
        "accept": "application/json",
        "x-api-key": api_token
    }

    response = requests.get(url, headers=headers)
    return response.json()


def payment_info(job_id,amount):

    amount = int(amount)
    url = f"https://api.xandar.instaleap.io/jobs/{job_id}/payment_info"

    payload = {
        "prices": {
            "attributes": [
                {
                    "type": "ORDER_VALUE",
                    "name": "payment",
                    "value": amount
                }
            ],
            "subtotal": 5,
            "shipping_fee": 0,
            "discounts": 0,
            "taxes": 0,
            "order_value": 5
        },
        "payment": {
            "payment_status": "SUCCEEDED",
            "method": "CASH",
            "metadata": { "newKey": "New Value" },
            "id": "string",
            "value": amount,
            "reference": "string",
            "blocking_policy": "CHECKOUT"
        },
        "invoice": {
            "reference": "teste",
            "attachments": ["www.teste.com"]
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_token
    }

    response = requests.put(url, json=payload, headers=headers)

    return response.json()