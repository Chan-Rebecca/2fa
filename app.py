from flask import Flask, render_template, request, redirect, session
import pyotp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'demo' and password == 'password':
            session['username'] = username
            return redirect('/2fa')
    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor_auth():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        otp = request.form['otp']
        if pyotp.TOTP("your_secret_otp_key").verify(otp):
            session['2fa_passed'] = True
            return redirect('/dashboard')
    return render_template('2fa.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session or '2fa_passed' not in session:
        return redirect('/')
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
