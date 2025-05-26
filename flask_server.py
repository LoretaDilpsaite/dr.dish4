from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medications.db'
db = SQLAlchemy(app)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active_ingredient = db.Column(db.String(100), nullable=False)
    atc_code = db.Column(db.String(20), nullable=False)
    application_scheme = db.Column(db.String(255))
    form = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    indication_code = db.Column(db.String(10))
    caution_info = db.Column(db.String(255))

@app.route('/api/medications', methods=['GET'])
def get_medications():
    meds = Medication.query.all()
    return jsonify([{
        'id': med.id,
        'name': med.name,
        'active_ingredient': med.active_ingredient,
        'atc_code': med.atc_code,
        'application_scheme': med.application_scheme,
        'form': med.form,
        'unit': med.unit,
        'indication_code': med.indication_code,
        'caution_info': med.caution_info
    } for med in meds])

@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    med = Medication(**data)
    db.session.merge(med)
    db.session.commit()
    return jsonify({"message": "Gespeichert"}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)
