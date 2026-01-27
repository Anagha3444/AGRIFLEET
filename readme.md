# FarmRide - Farmer Transportation Platform

A Python full-stack web application for farmers to book transportation for their produce to markets.

## Features

 **Booking System** - Farmers can book rides with pickup/drop locations
 **Product Selection** - Choose what you're transporting (vegetables, fruits, grains, dairy)
 **Driver Management** - View available drivers with ratings and prices
 **Real-time Tracking** - Track your ride status and driver location
 **Database** - SQLite database storing drivers and rides
 **REST API** - Backend APIs for all operations

## Tech Stack

**Backend:**
- Python 3.x
- Flask (Web framework)
- SQLite (Database)
- Flask-CORS (Cross-origin support)

**Frontend:**
- HTML5
- CSS3 (Custom styling)
- Vanilla JavaScript
- Fetch API for backend communication

## Project Structure

```
farmride-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── farmride.db           # SQLite database (auto-created)
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # All styling
│   └── js/
│       └── app.js        # Frontend logic
└── README.md
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
# Navigate to project folder
cd farmride-app

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Start the Flask server
python app.py
```

You should see:
```
 FarmRide Backend Starting...
 Server running at: http://127.0.0.1:5000
 Database: farmride.db
```

### 3. Open in Browser

Open your browser and go to:
```
http://127.0.0.1:5000
```

## How to Use

1. **Book a Ride:**
   - Enter pickup location (your farm)
   - Enter drop location (market/mandi)
   - Select product type
   - Click "Find Drivers"

2. **Choose Driver:**
   - View available drivers with ratings
   - See estimated price and arrival time
   - Click on a driver to book

3. **Track Ride:**
   - See ride confirmation
   - View trip details
   - Call driver if needed

## API Endpoints

### GET `/api/drivers`
Get all available drivers
```json
{
  "success": true,
  "drivers": [...]
}
```

### POST `/api/book-ride`
Book a ride with a driver
```json
{
  "pickup": "Farm Location",
  "dropoff": "Market",
  "product": "vegetables",
  "driver_id": 1,
  "price": 350
}
```

### GET `/api/ride/<ride_id>`
Get details of a specific ride

### GET `/api/rides`
Get all rides (admin view)

### POST `/api/calculate-fare`
Calculate estimated fare

## Database Schema

### Drivers Table
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- vehicle (TEXT)
- rating (REAL)
- available (INTEGER)
- phone (TEXT)

### Rides Table
- id (INTEGER PRIMARY KEY)
- pickup (TEXT)
- dropoff (TEXT)
- product (TEXT)
- driver_id (INTEGER)
- status (TEXT)
- price (REAL)
- created_at (TEXT)


## Features for College Demo

 Clean, professional UI
 Full booking flow
 Database integration
 REST API architecture
 Responsive design
 Easy to demonstrate
 Well-commented code

## Future Enhancements

- Google Maps integration for real tracking
- User authentication
- Payment gateway integration
- SMS notifications
- Admin dashboard
- Driver app
- Rating system


**Key Points to Mention:**
1. Full-stack Python web application
2. Uses Flask framework for backend
3. SQLite database for data persistence
4. RESTful API architecture
5. Clean separation of frontend/backend
6. Farmer-friendly interface
7. Solves real-world problem

**Demo Flow:**
1. Show the booking page
2. Fill in locations and select product
3. Show driver list with API call
4. Book a driver
5. Show tracking page
6. Explain the code structure
7. Show database entries

## Troubleshooting

**Port already in use:**
```bash
# Change port in app.py, line: app.run(port=5001)
```

**Module not found:**
```bash
pip install flask flask-cors
```

**Database issues:**
```bash
# Delete farmride.db and restart - it will be recreated
rm farmride.db
python app.py
```

