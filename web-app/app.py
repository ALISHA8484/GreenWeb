from flask import Flask, render_template, request, redirect, url_for, session, flash
from greenhouse import Greenhouse

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_change_this'

admin_config = {
    'username': 'admin',
    'password': 'IUTgreenhouses'
}

gh1 = Greenhouse(name="Greenhouse 1", port="/dev/serial0") 
gh2 = Greenhouse(name="Greenhouse 2", port="/dev/ttyAMA1")

greenhouses = {
    '1': gh1,
    '2': gh2
}

@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == admin_config['username'] and password == admin_config['password']:
            session['logged_in'] = True
            flash('Welcome back, Admin!', 'success') 
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', admin=admin_config)

@app.route('/update_account', methods=['POST'])
def update_account():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    
    if new_username and new_password:
        admin_config['username'] = new_username
        admin_config['password'] = new_password
        flash('Account updated successfully!', 'success')
    else:
        flash('Fields cannot be empty', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/greenhouse/<id>')
def greenhouse_detail(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    target_gh = greenhouses.get(id)
    
    if target_gh:
        sensor_data = target_gh.read_loop()
        #sensor_data = {'temp' : 27, 'hum' : 50, 'status' : 'Online'}
        
        return render_template('greenhouse_detail.html', gh=target_gh, data=sensor_data)
    else:
        return "Greenhouse not found", 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)