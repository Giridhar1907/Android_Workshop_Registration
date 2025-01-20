from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

EXCEL_FILE = "Registrations.xlsx"

# Ensure the Excel file exists with headers
if not os.path.exists(EXCEL_FILE):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Registrations"
    sheet.append(["Full Name", "Email", "Phone","Branch","Experience Level"])
    workbook.save(EXCEL_FILE)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json  # Get JSON data from the request
        print("Received Data:", data)  # Debugging

        full_name = data.get("fullName")
        email = data.get("email")
        phone = data.get("phone")
        branch = data.get("branch")
        experience = data.get("experience")
        

        # Ensure all fields are present
        if not all([full_name, email, phone,branch,experience]):
            return jsonify({"error": "Missing required fields"}), 400

        # Append data to Excel file
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active
        sheet.append([full_name, email, phone,branch,experience])
        workbook.save(EXCEL_FILE)

        print("Data stored successfully in Excel!")  # Debugging
        return jsonify({"message": "Registration Successful!"}), 200

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": "Failed to process the registration"}), 500

if __name__ == '__main__':
    app.run(debug=True)
