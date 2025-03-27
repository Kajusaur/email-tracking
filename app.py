from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

# Store tracking data (in-memory, does not modify CSV)
tracking_data = []

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Email Tracking Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { width: 80%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; cursor: pointer; }
            .opened { background-color: #c6efce; }
            input { margin-bottom: 10px; padding: 5px; width: 300px; }
        </style>
        <script>
            function searchTable() {
                let input = document.getElementById("searchInput").value.toLowerCase();
                let rows = document.querySelectorAll("tbody tr");
                rows.forEach(row => {
                    let text = row.innerText.toLowerCase();
                    row.style.display = text.includes(input) ? "" : "none";
                });
            }
            function sortTable(n) {
                let table = document.getElementById("trackingTable");
                let rows = Array.from(table.rows).slice(1);
                let sortedRows = rows.sort((a, b) => a.cells[n].innerText.localeCompare(b.cells[n].innerText));
                table.tBodies[0].append(...sortedRows);
            }
        </script>
        <meta http-equiv="refresh" content="10">
    </head>
    <body>
        <h2>Email Tracking Dashboard</h2>
        <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search emails, names, or companies...">
        <table id="trackingTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Email</th>
                    <th onclick="sortTable(1)">Name</th>
                    <th onclick="sortTable(2)">Company</th>
                    <th onclick="sortTable(3)">Opened At</th>
                </tr>
            </thead>
            <tbody>
                ''' + ''.join(f'<tr class="opened"><td>{entry["email"]}</td><td>{entry["name"]}</td><td>{entry["company"]}</td><td>{entry["time"]}</td></tr>' for entry in tracking_data) + '''
            </tbody>
        </table>
    </body>
    </html>
    '''

@app.route('/track')
def track():
    email = request.args.get("email")
    name = request.args.get("name", "Unknown")
    company = request.args.get("company", "Unknown")
    if email:
        tracking_data.append({"email": email, "name": name, "company": company, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return "", 204  # Return empty response (image tracking pixel)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
