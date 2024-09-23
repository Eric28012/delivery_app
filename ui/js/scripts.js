document.getElementById('checkAvailabilityBtn').addEventListener('click', checkAvailability);

async function checkAvailability() {
    try {
        const response = await fetch('http://localhost:5000/api_requests/check_availability', { method: 'GET' });
        const timeSlots = await response.json();
        renderTimeSlots(timeSlots);
    } catch (error) {
        alert('Error checking availability: ' + error.message);
    }
}

function renderTimeSlots(timeSlots) {
    const timeSlotsList = document.getElementById('timeSlots');
    timeSlotsList.innerHTML = '';

    timeSlots.forEach(slot => {
        const li = document.createElement('li');
        li.textContent = 'from: ' + slot.from.slice(0,-8) + ' to: ' + slot.to.slice(0,-8) + ' expiration at - ' + slot.expires_at.slice(0,-8);
        li.addEventListener('click', () => selectTimeSlot(slot.id));
        timeSlotsList.appendChild(li);
    });

    document.getElementById('availability').style.display = 'block';
}

let selectedSlotId = '';

function selectTimeSlot(slotId) {
    selectedSlotId = slotId;
    alert(`Selected Time Slot ID: ${selectedSlotId}`);
}

document.getElementById('createOrderBtn').addEventListener('click', createOrder);

async function createOrder() {
    if (selectedSlotId) {
        try {
            const response = await fetch('http://localhost:5000/api_requests/create_job', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ slot_id: selectedSlotId })
            });

            if (response.ok) {
                alert('Order created successfully for the time slot ID: ' + selectedSlotId);
                const data = await response.json();                    
                const jobid = data.job_id;
                await display_orders_details(jobid);
            } else {
                const errorData = await response.json();
                alert('Error creating order: ' + errorData.message);
            }
        } catch (error) {
            alert('Error creating order: ' + error.message);
        }
    } else {
        alert('Please select a time slot first!');
    }
}

async function display_orders_details(jobid) {
    try {
        const response = await fetch('http://localhost:5000/api_requests/display_orders_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ jobid: jobid }) 
        });

        if (response.ok) {
            const orderDetails = await response.json(); 
            renderOrderDetails(orderDetails, jobid);
        } else {
            alert('Error fetching order details');
        }
    } catch (error) {
        alert('Error fetching order details: ' + error.message);
    }
}

function renderOrderDetails(orderDetails, jobid) {
    const detailsSection = document.getElementById('orderDetails'); 
    detailsSection.innerHTML = ''; 

    const orderInfo = `
        <h2>Order Details</h2>
        <p><strong>Name:</strong> ${orderDetails.job_number}</p>
        <p><strong>Customer Id:</strong> ${orderDetails.client_id}</p>
        <p><strong>created_at:</strong> ${orderDetails.created_at}</p>
        <p><strong>state:</strong> ${orderDetails.state}</p>
        <p><strong>method:</strong> ${orderDetails.collect_with.method}</p>
        <p><strong>store:</strong> ${orderDetails.store.name}</p>

        <input type="text" id="amount" placeholder="Enter payment amount" />
        <button id="payButton">Pay</button>
    `;

    detailsSection.innerHTML = orderInfo; 

    document.getElementById('payButton').addEventListener('click', () => pagar(jobid));


}

function pagar(jobid) {
    const paymentAmount = document.getElementById('amount').value;
    
    if (!paymentAmount) {
        alert('Please enter a valid payment amount.');
        return;
    }

    handle_payment_info(jobid, paymentAmount);
}


async function handle_payment_info(jobid, amount) {
    try {
        const response = await fetch('http://localhost:5000/api_requests/handle_payment_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ jobid: jobid, amount: amount }) 
        });

        if (response.ok) {
            alert('Payment processed successfully!');
        } else {
            alert('Error processing payment');
        }
    } catch (error) {
        alert('Error processing payment: ' + error.message);
    }
}