from flask import Flask, request, render_template, make_response, redirect, url_for
import jwt
import datetime

app = Flask(__name__)

# Vulnerable: JWT secret exposed in frontend
JWT_SECRET = "stark_industries_super_secret_key_2024"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == 'admin_top_secret_123':
        # Create admin JWT token
        payload = {
            'username': 'admin',
            'role': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('auth_token', token)
        return resp
        
    elif username == 'guest' and password == 'guest123':
        # Create guest JWT token
        payload = {
            'username': 'guest',
            'role': 'guest',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('auth_token', token)
        return resp
    else:
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('auth_token')
    
    if not token:
        return redirect('/')
    
    try:
        # Verify JWT token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        
        if decoded['role'] == 'admin':
            return render_template('dashboard.html', user=decoded)
        else:
            return render_template('guest_dashboard.html', user=decoded)
            
    except jwt.ExpiredSignatureError:
        return redirect('/')
    except jwt.InvalidTokenError:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)