from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'vehicleservice123')

def get_db():
    conn = mysql.connector.connect(
        host=os.environ.get('MYSQLHOST', '127.0.0.1'),
        port=int(os.environ.get('MYSQLPORT', 3306)),
        user=os.environ.get('MYSQLUSER', 'root'),
        password=os.environ.get('MYSQLPASSWORD', 'Rohith@2006'),
        database=os.environ.get('MYSQLDATABASE', 'vehicle_service_db')
    )
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET'])
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login_post():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM Users WHERE Username = %s AND Password = %s',
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user'] = username
            return jsonify({'success': True, 'redirect': '/'}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/stats')
@login_required
def get_stats():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT COUNT(*) as total FROM Customer')
        total_customers = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM Vehicle')
        total_vehicles = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM Service')
        total_services = cursor.fetchone()['total']

        cursor.execute('SELECT SUM(Amount) as total FROM Bill')
        result = cursor.fetchone()
        total_revenue = float(result['total']) if result['total'] else 0

        cursor.close()
        conn.close()

        return jsonify({
            'total_customers': total_customers,
            'total_vehicles': total_vehicles,
            'total_services': total_services,
            'total_revenue': total_revenue
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers')
@login_required
def get_customers():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Customer')
        customers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(customers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehicles')
@login_required
def get_vehicles():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT v.*,
                   CONCAT(c.First_Name, ' ', c.Last_Name) as owner_name
            FROM Vehicle v
            JOIN Customer c ON v.CustomerID = c.CustomerID
        ''')
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(vehicles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mechanics')
@login_required
def get_mechanics():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Mechanic')
        mechanics = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(mechanics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services')
@login_required
def get_services():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT s.*,
                   v.Reg_No, v.Brand, v.Model,
                   CONCAT(c.First_Name, ' ', c.Last_Name) as customer_name,
                   m.Name as mechanic_name
            FROM Service s
            JOIN Vehicle v ON s.VehicleID = v.VehicleID
            JOIN Customer c ON v.CustomerID = c.CustomerID
            JOIN Mechanic m ON s.MechanicID = m.MechanicID
            ORDER BY s.Service_Date DESC
        ''')
        services = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(services)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bills')
@login_required
def get_bills():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT b.*,
                   s.Service_Type,
                   CONCAT(c.First_Name, ' ', c.Last_Name) as customer_name
            FROM Bill b
            JOIN Service s ON b.ServiceID = s.ServiceID
            JOIN Vehicle v ON s.VehicleID = v.VehicleID
            JOIN Customer c ON v.CustomerID = c.CustomerID
        ''')
        bills = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(bills)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services', methods=['POST'])
@login_required
def create_service():
    try:
        data = request.get_json()

        required_fields = ['vehicle_id', 'mechanic_id', 'service_date', 'mileage', 'service_type', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Service (VehicleID, MechanicID, Service_Date, Mileage, Service_Type, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            data['vehicle_id'],
            data['mechanic_id'],
            data['service_date'],
            data['mileage'],
            data['service_type'],
            data['status']
        ))
        conn.commit()
        service_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'service_id': service_id,
            'message': 'Service created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_users_table():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(50) NOT NULL UNIQUE,
                Password VARCHAR(50) NOT NULL
            )
        ''')

        cursor.execute('SELECT * FROM Users WHERE Username = %s', ('admin',))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO Users (Username, Password) VALUES (%s, %s)',
                ('admin', 'admin123')
            )
            conn.commit()
            print("✅ Default admin user created: admin / admin123")
        else:
            print("✅ Users table ready")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    create_users_table()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False
    )
