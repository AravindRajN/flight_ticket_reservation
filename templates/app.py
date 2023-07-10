from flask import Flask, render_template, redirect, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

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


# Booking tickets
@app.route('/book/<flight_code>')
def book(flight_code):
    if 'username' in session:
        if flight_code in flights and flights[flight_code]['seats'] > 0:
            flights[flight_code]['seats'] -= 1
            return render_template('confirmation.html', flight=flights[flight_code])
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


if __name__ == '__main__':
    app.run(debug=True)
