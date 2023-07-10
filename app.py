from flask import Flask, render_template, redirect, request, session
import random
import string
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
# Set a secret key for session management

# Database for storing flight details
flights = {
    'F001': {'name': 'Flight 001', 'seats': 60},
    'F002': {'name': 'Flight 002', 'seats': 60},
    'F003': {'name': 'Flight 003', 'seats': 60},
}

# Database for storing user details
users = {
    'admin': {'password': 'admin', 'admin': True},
}


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')


# User signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            return render_template('signup.html', error='Username already exists')
        else:
            users[username] = {'password': password, 'admin': False}
            session['username'] = username
            return redirect('/dashboard')
    
    return render_template('signup.html')


# User dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', flights=flights)
    else:
        return redirect('/login')


# Searching for flights
@app.route('/search', methods=['POST'])
def search():
    date = request.form['date']
    time = request.form['time']
    
    available_flights = []
    for flight_code, flight in flights.items():
        available_seats = flight['seats']
        if available_seats > 0:
            available_flights.append((flight_code, flight['name'], available_seats))
    
    return render_template('search.html', date=date, time=time, flights=available_flights)


@app.route('/book/<flight_code>')
def book(flight_code):
    if 'username' in session:
        if flight_code in flights and flights[flight_code]['seats'] > 0:
            # Perform the booking process and store the booking details
            # Replace the following lines with your booking logic
            booking_id = 1  # Placeholder for the booking ID
            flight_name = flights[flight_code]['name']
            seat_number = 'A1'  # Placeholder for the seat number
            
            # Update the available seats count
            flights[flight_code]['seats'] -= 1
            
            # Add the booking to the user's bookings (database or data source)
            # Replace the following line with your code to store the booking
            # bookings.append(booking)
            
            return render_template('confirmation.html', flight_code=flight_code, flight_name=flight_name, seat_number=seat_number, booking_id=booking_id)
        else:
            return redirect('/dashboard')
    else:
        return redirect('/login')





# User bookings
@app.route('/mybookings')
def mybookings():
    if 'username' in session:
        return render_template('mybookings.html')
    else:
        return redirect('/login')


# User logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password and users[username]['admin']:
            session['username'] = username
            return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error='Invalid username or password')
    
    return render_template('admin_login.html')


# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' in session and users[session['username']]['admin']:
        return render_template('admin_dashboard.html', flights=flights)
    else:
        return redirect('/admin')


# Add flights
@app.route('/admin/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username' in session and users[session['username']]['admin']:
        if request.method == 'POST':
            flight_code = request.form['flight_code']
            flight_name = request.form['flight_name']
            
            if flight_code in flights:
                return render_template('add_flight.html', error='Flight code already exists')
            else:
                flights[flight_code] = {'name': flight_name, 'seats': 60}
                return redirect('/admin/dashboard')
        
        return render_template('add_flight.html')
    else:
        return redirect('/admin')


# Remove flights
@app.route('/admin/remove_flight/<flight_code>')
def remove_flight(flight_code):
    if 'username' in session and users[session['username']]['admin']:
        if flight_code in flights:
            del flights[flight_code]
        
        return redirect('/admin/dashboard')
    else:
        return redirect('/admin')



if __name__ == '__main__':
    app.run(debug=True)
