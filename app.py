from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import requests

app = Flask(__name__)

# Google Form URL
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSde_y_aJGR5bWkyC83iaPvxXU3Ias3PxIwetlVq-YGrToRqSw/formResponse"

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the registration page (handles GET and POST)
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        city = request.form.get('city')

        # Validate input
        if not name or not phone or not city:
            return "All fields are required", 400

        # Send data to Google Form
        form_data = {
            'entry.2072056986': name,
            'entry.291075541': phone,
            'entry.1845336953': city
        }
        try:
            response = requests.post(GOOGLE_FORM_URL, data=form_data)
            if response.status_code != 200:
                print(f"Failed to submit to Google Form: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error submitting to Google Form: {e}")

        # Append to CSV
        # csv_file = 'details.csv'
        # file_exists = os.path.isfile(csv_file)
        # with open(csv_file, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     if not file_exists:
        #         writer.writerow(['Name', 'Phone', 'Address'])
        #     writer.writerow([name, phone, city])

        # Redirect back to index
        return redirect(url_for('index'))

    # Handle GET request (render registration.html)
    return render_template('Registration.html')

# Route to serve the video file (optional, for debugging)
@app.route('/static/RSETI_free.mp4')
def serve_video():
    return send_from_directory('static', 'RSETI_free.mp4')

if __name__ == '__main__':
    app.run(debug=True)
