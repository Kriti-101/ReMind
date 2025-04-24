from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock database - In-memory storage
mock_db = {
    'patient': {
        'P001': {
            'id': 'P001',
            'name': 'John Doe',
            'age': '45',
            'gender': 'Male',
            'address': '123 Main St',
            'phone': '555-1234',
            'email': 'john@example.com',
            'blood': 'O+',
            'weight': '75',
            'height': '180',
            'stage': 'Stable',
            'history': 'Hypertension',
            'latitude': '37.7749',
            'longitude': '-122.4194'
        },
        'P002': {
            'id': 'P002',
            'name': 'Jane Smith',
            'age': '32',
            'gender': 'Female',
            'address': '456 Oak Ave',
            'phone': '555-5678',
            'email': 'jane@example.com',
            'blood': 'A-',
            'weight': '62',
            'height': '165',
            'stage': 'Recovery',
            'history': 'None',
            'latitude': '37.7833',
            'longitude': '-122.4167'
        }
    },
    'details': {
        'P001': {
            'Location': {
                'location': 'Home',
                'latitude': '37.7749',
                'longitude': '-122.4194'
            },
            'Contacts': {
                'name': 'Mary Doe',
                'relation': 'Spouse',
                'phone': '555-4321'
            },
            'Prescription': {
                'pid': 'RX001',
                'id1': 'P001',
                'name': 'Metformin',
                'mor': 'Yes',
                'af': 'Yes',
                'eve': 'No',
                'qty': '500mg',
                'day': '30'
            }
        },
        'P002': {
            'Location': {
                'location': 'Hospital',
                'latitude': '37.7833',
                'longitude': '-122.4167'
            },
            'Contacts': {
                'name': 'Robert Smith',
                'relation': 'Brother',
                'phone': '555-8765'
            },
            'Prescription': {
                'pid': 'RX002',
                'id1': 'P002',
                'name': 'Amoxicillin',
                'mor': 'Yes',
                'af': 'No',
                'eve': 'Yes',
                'qty': '250mg',
                'day': '10'
            }
        }
    }
}

def readpatient(table):
    patient_list = []
    keys = ['id', 'name', 'age', 'gender', 'address', 'phone', 'email', 'blood', 'weight', 'height', 'stage', 'history', 'latitude', 'longitude']
    
    # Get data from mock database
    for patient_id, patient_data in mock_db[table].items():
        temp = []
        for key in keys:
            temp.append(patient_data.get(key, None))
        patient_list.append(temp)
    
    # Sort by ID
    patient_list = sorted(patient_list, key=lambda x: x[0])
    return patient_list

def addpatientdata(data, id1):
    # Add or update patient data in mock database
    mock_db['patient'][id1] = data
    
    # Initialize details if new patient
    if id1 not in mock_db['details']:
        mock_db['details'][id1] = {}

def deletedata(collection, document):
    # Remove from mock database
    if document in mock_db[collection]:
        del mock_db[collection][document]
    
    # Also remove details if it's a patient
    if collection == 'patient' and document in mock_db['details']:
        del mock_db['details'][document]

def addlocationdata(data, id1):
    # Ensure patient exists in details
    if id1 not in mock_db['details']:
        mock_db['details'][id1] = {}
    
    # Update location data
    mock_db['details'][id1]['Location'] = data
    
    # Also update main patient record
    if id1 in mock_db['patient']:
        mock_db['patient'][id1]['latitude'] = data['latitude']
        mock_db['patient'][id1]['longitude'] = data['longitude']

def addprescriptiondata(data, id1):
    # Ensure patient exists in details
    if id1 not in mock_db['details']:
        mock_db['details'][id1] = {}
    
    # Update prescription data
    mock_db['details'][id1]['Prescription'] = data

def addcontactdata(data, id1):
    # Ensure patient exists in details
    if id1 not in mock_db['details']:
        mock_db['details'][id1] = {}
    
    # Update contact data
    mock_db['details'][id1]['Contacts'] = data

def deletecontactdata(id1):
    # Remove contact data if exists
    if id1 in mock_db['details'] and 'Contacts' in mock_db['details'][id1]:
        del mock_db['details'][id1]['Contacts']

@app.route("/", methods=['GET', 'POST'])
def hello():
    result = readpatient("patient")
    return render_template("index.html", data=result)

@app.route("/home", methods=['GET', 'POST'])
def homepage():
    result = readpatient("patient")
    return render_template("index.html", data=result)

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("addpatient.html")

@app.route("/locations", methods=['GET', 'POST'])
def locations():
    return render_template("locations.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route("/homemap", methods=['GET', 'POST'])
def homemap():
    return render_template("homemapdata.html")

@app.route("/prescription", methods=['GET', 'POST'])
def prescription():
    return render_template("prescription.html")

@app.route("/editpatient", methods=['GET', 'POST'])
def editpatient():
    return render_template("editpatient.html")

@app.route("/addlocation", methods=['GET', 'POST'])
def add():
    return render_template("addlocation.html")

@app.route("/addcontact", methods=['GET', 'POST'])
def addcontactpage():
    return render_template("addcontact.html")

@app.route("/editcontact", methods=['GET', 'POST'])
def editcontact():
    return render_template("editcontact.html")

@app.route("/addprescription", methods=['GET', 'POST'])
def addprescriptionpage():
    return render_template("addprescription.html")

@app.route("/editprescription", methods=['GET', 'POST'])
def editprescription():
    return render_template("editprescription.html")

@app.route("/add-patient", methods=['GET', 'POST'])
def addpatient():
    if request.method == "POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        email = request.form["email"]
        blood = request.form["blood"]
        weight = request.form["weight"]
        age = request.form["age"]
        height = request.form["height"]
        stage = request.form["stage"]
        address = request.form["address"]
        phone = request.form["phone"]
        history = request.form["history"]
        gender = request.form["gender"]
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        data = {'id': id1, 'name': name, 'email': email, 'blood': blood, 'weight': weight, 'age': age, 
                'height': height, 'stage': stage, 'address': address, 'phone': phone, 'history': history, 
                'gender': gender, 'latitude': latitude, 'longitude': longitude}
        
        addpatientdata(data, id1)
        result = readpatient("patient")
    else:
        result = readpatient("patient")
    
    return render_template("index.html", data=result)

@app.route("/delete-patient", methods=['GET', 'POST'])
def deletepatient():
    if request.method == "POST":
        collection = "patient"
        id1 = request.form["id1"]
        deletedata(collection, id1)
    return render_template("editpatient.html")

@app.route("/add-location", methods=['GET', 'POST'])
def addlocation():
    if request.method == "POST":
        id1 = request.form["id1"]
        location = request.form["location"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        data = {'location': location, 'latitude': latitude, 'longitude': longitude}
        addlocationdata(data, id1)

    return render_template("addlocation.html")

@app.route("/add-contact", methods=['GET', 'POST'])
def addcontact():
    if request.method == "POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        relation = request.form["relation"]
        phone = request.form["phone"]

        data = {'name': name, 'relation': relation, 'phone': phone}
        addcontactdata(data, id1)

        # Prepare data for template
        list_data = [id1, name, phone, relation]

    return render_template("contact.html", data=list_data if request.method == "POST" else None)

@app.route("/delete-contact", methods=['GET', 'POST'])
def deletecontact():
    if request.method == "POST":
        id1 = request.form["id1"]
        deletecontactdata(id1)
    return render_template("editcontact.html")

@app.route("/update-contact", methods=['GET', 'POST'])
def updatecontact():
    if request.method == "POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        relation = request.form["relation"]
        phone = request.form["phone"]

        data = {'name': name, 'relation': relation, 'phone': phone}
        addcontactdata(data, id1)

    return render_template("editcontact.html")

@app.route("/add-prescription", methods=['GET', 'POST'])
def addprescription():
    if request.method == "POST":
        pid = request.form["pid"]
        id1 = request.form["id1"]
        name = request.form["name"]
        mor = request.form["mor"]
        af = request.form["af"]
        eve = request.form["eve"]
        qty = request.form["qty"]
        day = request.form["day"]

        data = {'pid': pid, 'id1': id1, 'name': name, 'mor': mor, 'af': af, 'eve': eve, 'qty': qty, 'day': day}
        addprescriptiondata(data, id1)

        # Prepare data for template
        list_data = [id1, pid, name, mor, af, eve, qty, day]

    return render_template("prescription.html", data=list_data if request.method == "POST" else None)

@app.route("/delete-prescription", methods=['GET', 'POST'])
def deleteprescription():
    if request.method == "POST":
        id1 = request.form["id1"]
        if id1 in mock_db['details'] and 'Prescription' in mock_db['details'][id1]:
            del mock_db['details'][id1]['Prescription']
    return render_template("editprescription.html")

@app.route("/update-prescription", methods=['GET', 'POST'])
def updateprescriptiondata():
    if request.method == "POST":
        pid = request.form["pid"]
        id1 = request.form["id1"]
        name = request.form["name"]
        mor = request.form["mor"]
        af = request.form["af"]
        eve = request.form["eve"]
        qty = request.form["qty"]
        day = request.form["day"]

        data = {'pid': pid, 'id1': id1, 'name': name, 'mor': mor, 'af': af, 'eve': eve, 'qty': qty, 'day': day}
        addprescriptiondata(data, id1)

    return render_template("editprescription.html")

@app.route("/update-patient", methods=['GET', 'POST'])
def updatepatientdata():
    if request.method == "POST":
        id1 = request.form["id1"]
        name = request.form["name"]
        email = request.form["email"]
        blood = request.form["blood"]
        weight = request.form["weight"]
        age = request.form["age"]
        height = request.form["height"]
        stage = request.form["stage"]
        address = request.form["address"]
        phone = request.form["phone"]
        history = request.form["history"]
        gender = request.form["gender"]
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        data = {'id': id1, 'name': name, 'email': email, 'blood': blood, 'weight': weight, 'age': age, 
                'height': height, 'stage': stage, 'address': address, 'phone': phone, 'history': history, 
                'gender': gender, 'latitude': latitude, 'longitude': longitude}
        
        addpatientdata(data, id1)

    return render_template("editpatient.html")

@app.route("/update-location", methods=['POST'])
def update_location():
    if request.method == "POST":
        id1 = request.form["id1"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        data = {'latitude': latitude, 'longitude': longitude}
        addlocationdata(data, id1)

        result = readpatient("patient")
        return render_template("index.html", data=result, message="Location updated successfully!")

# API routes to get data in JSON format (useful for AJAX calls)
@app.route("/api/patients", methods=['GET'])
def api_patients():
    result = readpatient("patient")
    return jsonify(result)

@app.route("/api/patient/<id>", methods=['GET'])
def api_patient(id):
    if id in mock_db['patient']:
        return jsonify(mock_db['patient'][id])
    return jsonify({"error": "Patient not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)