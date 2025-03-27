from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# Store tracking data (in-memory, does not modify CSV)
tracking_data = {}

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Email Tracking Dashboard</title>
        <style>
            table { width: 50%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .opened { background-color: #c6efce; }
        </style>
        <meta http-equiv="refresh" content="10">
    </head>
    <body>
        <h2>Email Tracking Dashboard</h2>
        <table>
            <tr>
                <th>Email</th>
                <th>Opened At</th>
            </tr>
            ''' + ''.join(f'<tr class="opened"><td>{email}</td><td>{time}</td></tr>' for email, time in tracking_data.items()) + '''
        </table>
    </body>
    </html>
    '''

@app.route('/track')
def track():
    email = request.args.get("email")
    if email:
        tracking_data[email] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "", 204  # Return empty response (image tracking pixel)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
