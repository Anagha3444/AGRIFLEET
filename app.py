from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('farmride.db')
    c = conn.cursor()
    
    # Drivers table
    c.execute('''CREATE TABLE IF NOT EXISTS drivers
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, 
                  vehicle TEXT, 
                  rating REAL, 
                  available INTEGER,
                  phone TEXT)''')
    
    # Rides table
    c.execute('''CREATE TABLE IF NOT EXISTS rides
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pickup TEXT,
                  dropoff TEXT,
                  product TEXT,
                  driver_id INTEGER,
                  status TEXT,
                  price REAL,
                  created_at TEXT,
                  FOREIGN KEY(driver_id) REFERENCES drivers(id))''')
    
    # Insert sample drivers if table is empty
    c.execute("SELECT COUNT(*) FROM drivers")
    if c.fetchone()[0] == 0:
        sample_drivers = [
            (1, 'Raju Singh', 'Tata Ace', 4.8, 1, '9876543210'),
            (2, 'Mohan Kumar', 'Bolero Pickup', 4.9, 1, '9876543211'),
            (3, 'Vikram Yadav', 'Mahindra Jeep', 4.7, 1, '9876543212'),
            (4, 'Suresh Patel', 'Eicher Truck', 4.6, 1, '9876543213'),
            (5, 'Ramesh Gupta', 'Ashok Leyland', 4.9, 1, '9876543214')
        ]
        c.executemany("INSERT INTO drivers VALUES (?,?,?,?,?,?)", sample_drivers)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# API Routes

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/drivers', methods=['GET'])
def get_available_drivers():
    """Get all available drivers"""
    conn = sqlite3.connect('farmride.db')
    c = conn.cursor()
    c.execute("SELECT * FROM drivers WHERE available = 1")
    drivers = c.fetchall()
    conn.close()
    
    # Format response
    driver_list = []
    for driver in drivers:
        driver_list.append({
            'id': driver[0],
            'name': driver[1],
            'vehicle': driver[2],
            'rating': driver[3],
            'available': driver[4],
            'phone': driver[5],
            'price': random.randint(300, 500),  # Random price for demo
            'eta': f'{random.randint(3, 15)} mins'
        })
    
    return jsonify({'success': True, 'drivers': driver_list})

@app.route('/api/book-ride', methods=['POST'])
def book_ride():
    """Book a ride with a driver"""
    data = request.json
    
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    product = data.get('product')
    driver_id = data.get('driver_id')
    price = data.get('price')
    
    if not all([pickup, dropoff, product, driver_id]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Insert ride into database
    conn = sqlite3.connect('farmride.db')
    c = conn.cursor()
    
    c.execute("""INSERT INTO rides (pickup, dropoff, product, driver_id, status, price, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (pickup, dropoff, product, driver_id, 'confirmed', price, datetime.now().isoformat()))
    
    ride_id = c.lastrowid
    
    # Get driver details
    c.execute("SELECT * FROM drivers WHERE id = ?", (driver_id,))
    driver = c.fetchone()
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'ride_id': ride_id,
        'driver': {
            'id': driver[0],
            'name': driver[1],
            'vehicle': driver[2],
            'rating': driver[3],
            'phone': driver[5]
        },
        'message': 'Ride booked successfully!'
    })

@app.route('/api/ride/<int:ride_id>', methods=['GET'])
def get_ride_details(ride_id):
    """Get details of a specific ride"""
    conn = sqlite3.connect('farmride.db')
    c = conn.cursor()
    
    c.execute("""SELECT r.*, d.name, d.vehicle, d.phone 
                 FROM rides r 
                 JOIN drivers d ON r.driver_id = d.id 
                 WHERE r.id = ?""", (ride_id,))
    
    ride = c.fetchone()
    conn.close()
    
    if not ride:
        return jsonify({'success': False, 'message': 'Ride not found'}), 404
    
    return jsonify({
        'success': True,
        'ride': {
            'id': ride[0],
            'pickup': ride[1],
            'dropoff': ride[2],
            'product': ride[3],
            'status': ride[5],
            'price': ride[6],
            'driver': {
                'name': ride[8],
                'vehicle': ride[9],
                'phone': ride[10]
            }
        }
    })

@app.route('/api/rides', methods=['GET'])
def get_all_rides():
    """Get all rides for admin view"""
    conn = sqlite3.connect('farmride.db')
    c = conn.cursor()
    
    c.execute("""SELECT r.*, d.name, d.vehicle 
                 FROM rides r 
                 JOIN drivers d ON r.driver_id = d.id 
                 ORDER BY r.created_at DESC""")
    
    rides = c.fetchall()
    conn.close()
    
    ride_list = []
    for ride in rides:
        ride_list.append({
            'id': ride[0],
            'pickup': ride[1],
            'dropoff': ride[2],
            'product': ride[3],
            'driver_name': ride[8],
            'vehicle': ride[9],
            'status': ride[5],
            'price': ride[6],
            'created_at': ride[7]
        })
    
    return jsonify({'success': True, 'rides': ride_list})

@app.route('/api/calculate-fare', methods=['POST'])
def calculate_fare():
    """Calculate estimated fare based on distance"""
    data = request.json
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    
    # Simple fare calculation (in real app, use Google Maps Distance Matrix API)
    base_fare = 100
    per_km = 15
    estimated_km = random.randint(10, 30)  # Random for demo
    total_fare = base_fare + (per_km * estimated_km)
    
    return jsonify({
        'success': True,
        'estimated_fare': total_fare,
        'estimated_km': estimated_km,
        'base_fare': base_fare,
        'per_km': per_km
    })

if __name__ == '__main__':
    print("FarmRide Backend Starting...")
    print("Server running at: http://127.0.0.1:5000")
    print("Database: farmride.db")
    app.run(debug=True, host='0.0.0.0', port=5000)