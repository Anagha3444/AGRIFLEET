#  FarmRide Backend API Documentation

Base URL: `http://localhost:5000`

---

## Table of Contents
1. [Get Available Drivers](#1-get-available-drivers)
2. [Book a Ride](#2-book-a-ride)
3. [Get Ride Details](#3-get-ride-details)
4. [Get All Rides](#4-get-all-rides)
5. [Calculate Fare](#5-calculate-fare)

---

## 1. Get Available Drivers

**Endpoint:** `GET /api/drivers`

**Description:** Returns list of all available drivers

**Request:** No body required

**Response:**
```json
{
    "success": true,
    "drivers": [
        {
            "id": 1,
            "name": "Raju Singh",
            "vehicle": "Tata Ace",
            "rating": 4.8,
            "available": 1,
            "phone": "9876543210",
            "price": 450,
            "eta": "5 mins"
        },
        {
            "id": 2,
            "name": "Mohan Kumar",
            "vehicle": "Bolero Pickup",
            "rating": 4.9,
            "available": 1,
            "phone": "9876543211",
            "price": 380,
            "eta": "8 mins"
        }
    ]
}
```

**Frontend Example:**
```javascript
fetch('http://localhost:5000/api/drivers')
    .then(response => response.json())
    .then(data => {
        console.log(data.drivers);
    });
```

---

## 2. Book a Ride

**Endpoint:** `POST /api/book-ride`

**Description:** Book a new ride with a driver

**Request Body:**
```json
{
    "pickup": "Village Market",
    "dropoff": "City Center",
    "product": "Tomatoes - 50kg",
    "driver_id": 1,
    "price": 450
}
```

**Required Fields:**
- `pickup` (string): Pickup location
- `dropoff` (string): Drop-off location
- `product` (string): Product/cargo description
- `driver_id` (integer): ID of selected driver
- `price` (number): Agreed price

**Success Response:**
```json
{
    "success": true,
    "ride_id": 123,
    "driver": {
        "id": 1,
        "name": "Raju Singh",
        "vehicle": "Tata Ace",
        "rating": 4.8,
        "phone": "9876543210"
    },
    "message": "Ride booked successfully!"
}
```

**Error Response:**
```json
{
    "success": false,
    "message": "Missing required fields"
}
```

**Frontend Example:**
```javascript
const bookingData = {
    pickup: "Village Market",
    dropoff: "City Center",
    product: "Tomatoes - 50kg",
    driver_id: 1,
    price: 450
};

fetch('http://localhost:5000/api/book-ride', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(bookingData)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Ride booked! ID:', data.ride_id);
    }
});
```

---

## 3. Get Ride Details

**Endpoint:** `GET /api/ride/<ride_id>`

**Description:** Get details of a specific ride

**Example:** `GET /api/ride/123`

**Response:**
```json
{
    "success": true,
    "ride": {
        "id": 123,
        "pickup": "Village Market",
        "dropoff": "City Center",
        "product": "Tomatoes - 50kg",
        "status": "confirmed",
        "price": 450,
        "driver": {
            "name": "Raju Singh",
            "vehicle": "Tata Ace",
            "phone": "9876543210"
        }
    }
}
```

**Frontend Example:**
```javascript
const rideId = 123;

fetch(`http://localhost:5000/api/ride/${rideId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data.ride);
    });
```

---

## 4. Get All Rides

**Endpoint:** `GET /api/rides`

**Description:** Get all rides (for admin dashboard)

**Response:**
```json
{
    "success": true,
    "rides": [
        {
            "id": 123,
            "pickup": "Village Market",
            "dropoff": "City Center",
            "product": "Tomatoes - 50kg",
            "driver_name": "Raju Singh",
            "vehicle": "Tata Ace",
            "status": "confirmed",
            "price": 450,
            "created_at": "2024-01-15T10:30:00"
        }
    ]
}
```

**Frontend Example:**
```javascript
fetch('http://localhost:5000/api/rides')
    .then(response => response.json())
    .then(data => {
        data.rides.forEach(ride => {
            console.log(`Ride #${ride.id}: ${ride.status}`);
        });
    });
```

---

## 5. Calculate Fare

**Endpoint:** `POST /api/calculate-fare`

**Description:** Calculate estimated fare for a route

**Request Body:**
```json
{
    "pickup": "Village Market",
    "dropoff": "City Center"
}
```

**Response:**
```json
{
    "success": true,
    "estimated_fare": 450,
    "estimated_km": 20,
    "base_fare": 100,
    "per_km": 15
}
```

**Frontend Example:**
```javascript
const fareData = {
    pickup: "Village Market",
    dropoff: "City Center"
};

fetch('http://localhost:5000/api/calculate-fare', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(fareData)
})
.then(response => response.json())
.then(data => {
    console.log(`Estimated fare: ₹${data.estimated_fare}`);
});
```

---

## 🔧 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (missing fields) |
| 404 | Not Found (ride/driver doesn't exist) |
| 500 | Server Error |

---

## 🚀 Testing with Postman

1. Open Postman
2. Create new request
3. Set method (GET/POST)
4. Enter URL (e.g., `http://localhost:5000/api/drivers`)
5. For POST: Go to Body → raw → JSON
6. Paste request body
7. Click Send

---

## 📝 Notes for Frontend Team

### Important:
- Backend runs on `http://localhost:5000`
- Always use exact field names (e.g., `driver_id` not `driverId`)
- All POST requests need `Content-Type: application/json` header
- Check `success` field in response before accessing data

### CORS:
Backend has CORS enabled, so frontend can run on different port (e.g., 3000, 8080)

### Error Handling:
```javascript
fetch(url, options)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Handle success
        } else {
            // Show error: data.message
        }
    })
    .catch(error => {
        console.error('Network error:', error);
    });
```

---

## Troubleshooting

**Problem:** Cannot connect to backend
-  Check if backend is running (`python app.py`)
-  Check URL is correct (`http://localhost:5000`)

**Problem:** "Missing required fields" error
-  Check all field names match exactly
-  Check you're sending JSON format
-  Check Content-Type header is set

**Problem:** CORS error
-  Make sure `flask-cors` is installed
-  Check CORS is enabled in app.py

---

