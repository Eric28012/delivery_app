from flask import Flask, jsonify, request
from flask_cors import CORS
from api_requests import *

app = Flask(__name__)

CORS(app)

@app.route('/api_requests/check_availability', methods=['GET'])
def handle_check_availability():
    availability = check_availability()  
    return jsonify(availability) 

@app.route('/api_requests/create_job', methods=['POST'])
def handle_create_job():
    data = request.get_json() 
    slot_id = data.get('slot_id')
    
    job = create_job(slot_id)  
    return jsonify(job) 


@app.route('/api_requests/display_orders_details', methods=['POST'])
def handle_display_order():
    data = request.get_json()
    jobid = data.get('jobid')
    order_details = display_orders_details(jobid)
    return jsonify(order_details) 


@app.route('/api_requests/handle_payment_info', methods=['POST'])
def handle_payment_info():
    data = request.get_json()
    job_id = data.get('jobid')
    amount = data.get('amount')

    if not job_id or not amount:
        return jsonify({"error": "Missing job_id or amount"}), 400

    payment_response = payment_info(job_id,amount)

    return jsonify(payment_response), 200


if __name__ == '__main__':
    app.run(debug=True)
