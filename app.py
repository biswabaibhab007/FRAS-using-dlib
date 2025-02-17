from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', selected_date=today_date, no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return jsonify({'status': 'no_data', 'message': 'No attendance data found for this date.'})

    return jsonify({'status': 'success', 'attendance_data': attendance_data})

if __name__ == '__main__':
    app.run(debug=True)
