from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    print("🚀 Route was hit!")

    if request.method == 'POST':
        data = {
            "Date": str(date.today()),
            "Client": request.form['client'],
            "Package": request.form['package'],
            "Revenue": float(request.form['revenue']),
            "Lead Name": request.form['lead_name'],
            "Lead Date": request.form['lead_date'],
            "Lead Source": request.form['lead_source'],
            "Consultation Name": request.form['consult_name'],
            "Consultation Outcome": request.form['consult_outcome'],
            "Consultation Source": request.form['consult_source'],
            "Opportunity Name": request.form['opp_name'],
            "Opportunity Provider": request.form['opp_provider'],
            "Opportunity Desc": request.form['opp_desc'],
            "Attendance Done": int(request.form['attendance']),
            "No Shows": int(request.form['no_shows'])
        }

        os.makedirs('../data', exist_ok=True)
        file_path = '../data/reports.xlsx'

        # Create individual DataFrames
        sales_df = pd.DataFrame([{
            "Date": data["Date"],
            "Client": data["Client"],
            "Package": data["Package"],
            "Revenue": data["Revenue"]
        }])

        leads_df = pd.DataFrame([{
            "Date": data["Date"],
            "Lead Name": data["Lead Name"],
            "Lead Date": data["Lead Date"],
            "Lead Source": data["Lead Source"]
        }])

        opportunities_df = pd.DataFrame([{
            "Date": data["Date"],
            "Opportunity Name": data["Opportunity Name"],
            "Opportunity Provider": data["Opportunity Provider"],
            "Opportunity Desc": data["Opportunity Desc"]
        }])

        consultations_df = pd.DataFrame([{
            "Date": data["Date"],
            "Consultation Name": data["Consultation Name"],
            "Consultation Outcome": data["Consultation Outcome"],
            "Consultation Source": data["Consultation Source"]
        }])

        attendance_df = pd.DataFrame([{
            "Date": data["Date"],
            "Attendance Done": data["Attendance Done"],
            "No Shows": data["No Shows"]
        }])

        # Append or create new Excel with sheets
        if os.path.exists(file_path):
            try: sales_existing = pd.read_excel(file_path, sheet_name="Sales")
            except: sales_existing = pd.DataFrame()

            try: leads_existing = pd.read_excel(file_path, sheet_name="Leads")
            except: leads_existing = pd.DataFrame()

            try: opp_existing = pd.read_excel(file_path, sheet_name="Opportunities")
            except: opp_existing = pd.DataFrame()

            try: consult_existing = pd.read_excel(file_path, sheet_name="Consultations")
            except: consult_existing = pd.DataFrame()

            try: att_existing = pd.read_excel(file_path, sheet_name="Attendance")
            except: att_existing = pd.DataFrame()

            sales_combined = pd.concat([sales_existing, sales_df], ignore_index=True)
            leads_combined = pd.concat([leads_existing, leads_df], ignore_index=True)
            opp_combined = pd.concat([opp_existing, opportunities_df], ignore_index=True)
            consult_combined = pd.concat([consult_existing, consultations_df], ignore_index=True)
            att_combined = pd.concat([att_existing, attendance_df], ignore_index=True)

            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                sales_combined.to_excel(writer, sheet_name="Sales", index=False)
                leads_combined.to_excel(writer, sheet_name="Leads", index=False)
                opp_combined.to_excel(writer, sheet_name="Opportunities", index=False)
                consult_combined.to_excel(writer, sheet_name="Consultations", index=False)
                att_combined.to_excel(writer, sheet_name="Attendance", index=False)
        else:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                sales_df.to_excel(writer, sheet_name="Sales", index=False)
                leads_df.to_excel(writer, sheet_name="Leads", index=False)
                opportunities_df.to_excel(writer, sheet_name="Opportunities", index=False)
                consultations_df.to_excel(writer, sheet_name="Consultations", index=False)
                attendance_df.to_excel(writer, sheet_name="Attendance", index=False)

        return "✅ Report submitted successfully!"

    return render_template('form.html')

# ✅ Enable access from iPad or any local network device
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')




