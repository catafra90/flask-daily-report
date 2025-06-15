from flask import Flask, render_template, request, redirect, session, send_file
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/4ZsvACAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=QAsMtcgO05jwCeg2HXcDrCK7ngmtq0vpQwguobG8-vU"

file_path = os.path.join("data", "reports.xlsx")
os.makedirs("data", exist_ok=True)

# === INITIALIZE EXCEL FILE ===
if not os.path.exists(file_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Date", "Client Name", "Package", "Revenue"])
    wb.create_sheet(title="Leads").append(["Date", "Lead Name", "Lead Date", "Lead Source"])
    wb.create_sheet(title="Consultation").append(["Date", "Consultation Name", "Consultation Outcome", "Consultation Source"])
    wb.create_sheet(title="Opportunity").append(["Date", "Opportunity Name", "Opportunity Provider", "Opportunity Description"])
    wb.create_sheet(title="Attendance").append(["Date", "Attendances Done", "No Show"])
    wb.save(file_path)

# === PLATFORM ROUTES ===

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return "<h2>📊 Analytics Page – Coming Soon</h2>"

@app.route('/automation')
def automation():
    return "<h2>🧠 Automation Page – Coming Soon</h2>"

@app.route('/clients')
def clients():
    return "<h2>👥 Clients Page – Coming Soon</h2>"

@app.route('/scheduling')
def scheduling():
    return "<h2>📅 Scheduling Page – Coming Soon</h2>"

# === DAILY REPORT FLOW ===

@app.route('/daily-report', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        session['sales'] = request.form.to_dict(flat=False)
        return redirect('/leads')
    return render_template('step1_sales.html', session_data=session.get('sales'))

@app.route('/leads', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        session['leads'] = request.form.to_dict(flat=False)
        return redirect('/consultations')
    return render_template('step2_leads.html', session_data=session.get('leads'))

@app.route('/consultations', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        session['consultations'] = request.form.to_dict(flat=False)
        return redirect('/opportunities')
    return render_template('step3_consultation.html', session_data=session.get('consultations'))

@app.route('/opportunities', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        session['opportunities'] = request.form.to_dict(flat=False)
        return redirect('/attendance')
    return render_template('step4_opportunity.html', session_data=session.get('opportunities'))

@app.route('/attendance', methods=['GET', 'POST'])
def step5():
    if request.method == 'POST':
        session['attendance'] = request.form.to_dict()
        wb = load_workbook(file_path)

        sales = session.get('sales', {})
        leads = session.get('leads', {})
        consultations = session.get('consultations', {})
        opportunities = session.get('opportunities', {})
        attendance = session.get('attendance', {})

        sales_ws = wb["Sales"]
        leads_ws = wb["Leads"]
        consultation_ws = wb["Consultation"]
        opportunity_ws = wb["Opportunity"]
        attendance_ws = wb["Attendance"]

        chat_message = [f"*\U0001F4C5 Daily Report - {datetime.now().date()}*\n"]

        # SALES
        chat_message.append("*\U0001F4E6 Sales*\n_Client Name | Package | Revenue_")
        for i in range(len(sales.get('client_name', []))):
            client = sales.get('client_name', [''])[i].strip()
            package = sales.get('package', [''])[i].strip()
            revenue = sales.get('revenue', [''])[i].strip()
            if client or package or revenue:
                sales_ws.append([datetime.now().date(), client, package, revenue])
                chat_message.append(f"- {client} | {package} | {revenue}")

        # LEADS
        chat_message.append("\n*\U0001F4CB Leads*\n_Lead Name | Lead Date | Lead Source_")
        for i in range(len(leads.get('lead_name', []))):
            name = leads.get('lead_name', [''])[i].strip()
            date = leads.get('lead_date', [''])[i].strip()
            source = leads.get('lead_source', [''])[i].strip()
            if name or date or source:
                leads_ws.append([datetime.now().date(), name, date, source])
                chat_message.append(f"- {name} | {date} | {source}")

        # CONSULTATIONS
        chat_message.append("\n*\U0001F4AC Consultations*\n_Consultation Name | Outcome | Source_")
        for i in range(len(consultations.get('consultation_name', []))):
            name = consultations.get('consultation_name', [''])[i].strip()
            outcome = consultations.get('consultation_outcome', [''])[i].strip()
            source = consultations.get('consultation_source', [''])[i].strip()
            if name or outcome or source:
                consultation_ws.append([datetime.now().date(), name, outcome, source])
                chat_message.append(f"- {name} | {outcome} | {source}")

        # OPPORTUNITIES
        chat_message.append("\n*\U0001F31F Opportunities*\n_Opportunity Name | Provider | Description_")
        for i in range(len(opportunities.get('opportunity_name', []))):
            name = opportunities.get('opportunity_name', [''])[i].strip()
            provider = opportunities.get('opportunity_provider', [''])[i].strip()
            description = opportunities.get('opportunity_description', [''])[i].strip()
            if name or provider or description:
                opportunity_ws.append([datetime.now().date(), name, provider, description])
                chat_message.append(f"- {name} | {provider} | {description}")

        # ATTENDANCE
        attended = attendance.get('attended', '').strip()
        no_show = attendance.get('no_show', '').strip()
        if attended or no_show:
            attendance_ws.append([datetime.now().date(), attended, no_show])
            chat_message.append("\n*\U0001F4CA Attendance*\n_Attendances Done | No Show_")
            chat_message.append(f"- {attended} | {no_show}")

        wb.save(file_path)
        session.clear()

        try:
            requests.post(CHAT_WEBHOOK_URL, json={"text": "\n".join(chat_message)})
        except Exception as e:
            print("❌ Failed to send to Google Chat:", e)

        return "✅ Report Submitted"

    return render_template('step5_attendance.html', session_data=session.get('attendance'))

@app.route('/download-report')
def download_report():
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "⚠️ No report found."

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')

