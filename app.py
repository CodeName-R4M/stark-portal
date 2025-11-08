from flask import Flask, request, render_template, make_response, redirect, url_for, jsonify
import jwt
import datetime
import os

app = Flask(__name__)

# Vulnerable: JWT secret exposed in frontend
JWT_SECRET = "stark_industries_super_secret_key_2024"

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stark Industries - JWT Portal</title>
        <style>
            body { background: #0a0a2a; color: #00f0ff; font-family: Arial; margin: 0; padding: 20px; }
            .container { max-width: 500px; margin: 50px auto; padding: 30px; background: rgba(10,15,30,0.9); border-radius: 10px; border: 1px solid #00f0ff; }
            input, button { padding: 10px; margin: 5px; width: 100%; background: #1a1a2e; color: #00f0ff; border: 1px solid #00f0ff; border-radius: 5px; }
            button:hover { background: #00f0ff; color: #0a0a2a; }
        </style>
        <script>
            // Vulnerable: JWT secret exposed in client-side code
            const JWT_SECRET = "stark_industries_super_secret_key_2024";
            console.log("Debug: JWT System Initialized");
            console.log("Security Note: JWT operations use key - " + JWT_SECRET);
        </script>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Stark Industries JWT Portal</h1>
            <form action="/login" method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p><small>Guest access: guest / guest123</small></p>
        </div>
    </body>
    </html>
    '''

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
            return f'''
            <div style="max-width: 600px; margin: 50px auto; padding: 30px; background: #0a0a2a; color: #00f0ff; border: 2px solid #00ff00;">
                <h1>🔓 Admin Dashboard</h1>
                <p>Welcome, {decoded['username']}!</p>
                <div style="background: #001a00; padding: 20px; border: 1px solid #00ff00;">
                    <h3>🚩 FLAG: npflag{{jwt_s3cr3t_3xp0s3d_w1n}}</h3>
                    <p>System Access: FULL</p>
                    <p>Security Level: MAXIMUM</p>
                </div>
            </div>
            '''
        else:
            return f'''
            <div style="max-width: 600px; margin: 50px auto; padding: 30px; background: #0a0a2a; color: #00f0ff; border: 2px solid #ff4444;">
                <h1>🔒 Guest Dashboard</h1>
                <p>Welcome, {decoded['username']}!</p>
                <p>Your access is limited. Administrator role required.</p>
                <p style="color: #ff4444;">Current Role: {decoded['role']}</p>
                <p>Access Denied: Insufficient permissions</p>
            </div>
            '''
            
    except jwt.ExpiredSignatureError:
        return redirect('/')
    except jwt.InvalidTokenError:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)