from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Function to identify suspicious beneficiaries
def analyze_records(data):
    # Rule 1: Low income but high benefits
    condition1 = (data['Income'] < 20000) & (data['Benefits'] > 30000)
    
    # Rule 2: Benefits are more than twice the income
    condition2 = data['Benefits'] > (data['Income'] * 2)
    
    # Combine both conditions
    suspicious_data = data[condition1 | condition2]
    
    return suspicious_data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    
    # Read CSV file
    dataset = pd.read_csv(uploaded_file)
    
    # Analyze data
    results = analyze_records(dataset)
    
    # Display output
    if results.empty:
        return "<h3>No suspicious beneficiaries found ✅</h3>"
    else:
        return "<h3>Suspicious Beneficiaries 🚨</h3>" + results.to_html(index=False)


if __name__ == "__main__":
    app.run(debug=True)