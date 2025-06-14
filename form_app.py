print("🚀 Starting form_app.py on Render")

from flask import Flask, request, render_template_string, send_file
import os
from datetime import datetime
from openpyxl import Workbook, load_workbook
import requests

app = Flask(__name__)

CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/4ZsvACAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=QAsMtcgO05jwCeg2HXcDrCK7ngmtq0vpQwguobG8-vU"

def save_report_to_excel(data):
    print("📝 Saving to Excel...")
    file_path = os.path.join("data", "reports.xlsx")
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(file_path):
        wb = Workbook()
        ws = wb.active
        ws.append([
            "Timestamp", "Client Name", "Package", "Revenue",
            "Lead Name", "Lead Date", "Lead Source",
            "Consultation Name", "Consultation Outcome", "Consultation Source",
            "Opportunity Name", "Opportunity Provider", "Opportunity Description",
            "Attendances Done", "No Show"
        ])
    else:
        wb = load_workbook(file_path)
        ws = wb.active

    ws.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("client_name"),
        data.get("package"),
        data.get("revenue"),
        data.get("lead_name"),
        data.get("lead_date"),
        data.get("lead_source"),
        data.get("consultation_name"),
        data.get("consultation_outcome"),
        data.get("consultation_source"),
        data.get("opportunity_name"),
        data.get("opportunity_provider"),
        data.get("opportunity_description"),
        data.get("attendance_done"),
        data.get("no_show"),
    ])

    wb.save(file_path)
    print("✅ Excel saved at:", os.path.abspath(file_path))

def send_to_google_chat(data):
    print("📤 Sending to Google Chat...")
    message = {
        "text": (
            "📋 *Daily Report Submitted*\n"
            f"👤 Client: {data.get('client_name')}\n"
            f"💰 Revenue: ${data.get('revenue')}\n"
            f"📦 Package: {data.get('package')}"
        )
    }
    try:
        response = requests.post(CHAT_WEBHOOK_URL, json=message)
        print("✅ Google Chat Response:", response.status_code)
    except Exception as e:
        print("❌ Google Chat Error:", e)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Daily Report</title>
        <style>
            body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; }
            .section { display: none; padding: 20px; border-radius: 10px; background: #f1f1f1; }
            .section.active { display: block; }
            textarea { width: 100%; padding: 10px; font-size: 16px; margin-bottom: 10px; }
            button, input[type=submit] {
                padding: 10px 20px;
                margin: 5px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
        </style>
        <script>
            let current = 0;
            function show(index) {
                const sections = document.querySelectorAll(".section");
                sections.forEach((s, i) => s.classList.toggle("active", i === index));
            }
            function next() { if (current < 4) current++; show(current); }
            function prev() { if (current > 0) current--; show(current); }
            window.onload = () => show(0);
        </script>
    </head>
    <body>
        <h2>📋 Daily Report</h2>
        <form method="POST" action="/submit">
            <div class="section">
                <h3>Sales</h3>
                <textarea name="client_name" placeholder="Client Name"></textarea>
                <textarea name="package" placeholder="Package Sold"></textarea>
                <textarea name="revenue" placeholder="Revenue ($)"></textarea>
                <button type="button" onclick="next()">Next →</button>
            </div>
            <div class="section">
                <h3>Leads</h3>
                <textarea name="lead_name" placeholder="Lead Name"></textarea>
                <textarea name="lead_date" placeholder="Lead Date"></textarea>
                <textarea name="lead_source" placeholder="Lead Source"></textarea>
                <button type="button" onclick="prev()">← Back</button>
                <button type="button" onclick="next()">Next →</button>
            </div>
            <div class="section">
                <h3>Consultations</h3>
                <textarea name="consultation_name" placeholder="Consultation Name"></textarea>
                <textarea name="consultation_outcome" placeholder="Outcome"></textarea>
                <textarea name="consultation_source" placeholder="Source"></textarea>
                <button type="button" onclick="prev()">← Back</button>
                <button type="button" onclick="next()">Next →</button>
            </div>
            <div class="section">
                <h3>Opportunities</h3>
                <textarea name="opportunity_name" placeholder="Opportunity Name"></textarea>
                <textarea name="opportunity_provider" placeholder="Provider"></textarea>
                <textarea name="opportunity_description" placeholder="Description"></textarea>
                <button type="button" onclick="prev()">← Back</button>
                <button type="button" onclick="next()">Next →</button>
            </div>
            <div class="section">
                <h3>Attendance</h3>
                <textarea name="attendance_done" placeholder="Attendances Done"></textarea>
                <textarea name="no_show" placeholder="No Show"></textarea>
                <button type="button" onclick="prev()">← Back</button>
                <input type="submit" value="✅ Submit Report">
            </div>
        </form>
    </body>
    </html>
    ''')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    print("📥 Received data:", data)
    save_report_to_excel(data)
    send_to_google_chat(data)
    return "✅ Report submitted successfully!"

@app.route('/download-report')
def download_report():
    file_path = os.path.join("data", "reports.xlsx")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "⚠️ No report found."





