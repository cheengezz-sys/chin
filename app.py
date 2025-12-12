# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from models import (
    Patient, Doctor, Visit, Service, Tooth, PatientTooth,
    Payment  # ← Критически важный импорт, без него была ошибка NameError
)
from forms import PatientForm, VisitForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dental_clinic_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ——— Routes ———

@app.route('/')
def index():
    # Агрегация: общее количество и сумма оплат
    stats = {
        'patients': Patient.query.count(),
        'doctors': Doctor.query.count(),
        'visits': Visit.query.count(),
        'services': Service.query.count(),
        'revenue_cents': db.session.query(db.func.coalesce(db.func.sum(Payment.AmountCents), 0)).scalar()
    }
    stats['revenue'] = f"{stats['revenue_cents'] / 100:.2f}"
    return render_template('index.html', stats=stats)


# — Patients —
@app.route('/patients')
def patients_list():
    patients = Patient.query.order_by(Patient.FullName).all()
    return render_template('patients/list.html', patients=patients)


@app.route('/patients/new', methods=['GET', 'POST'])
def patient_create():
    form = PatientForm()
    if form.validate_on_submit():
        # Проверка уникальности телефона
        if Patient.query.filter_by(Phone=form.phone.data).first():
            flash(f"⚠️ Пациент с телефоном {form.phone.data} уже существует!", "danger")
        else:
            patient = Patient(
                FullName=form.full_name.data.strip(),
                BirthDate=form.birth_date.data,
                Phone=form.phone.data,
                Email=form.email.data or None,
                Address=form.address.data or None
            )
            db.session.add(patient)
            db.session.commit()
            flash(f"✅ Пациент «{patient.FullName}» успешно добавлен!", "success")
            return redirect(url_for('patients_list'))
    return render_template('patients/create.html', form=form)


@app.route('/patients/<int:pid>')
def patient_detail(pid):
    patient = Patient.query.get_or_404(pid)
    visits = Visit.query.filter_by(PatientID=pid).order_by(Visit.VisitDateTime.desc()).all()
    teeth = db.session.query(PatientTooth, Tooth).join(Tooth).filter(PatientTooth.PatientID == pid).all()
    return render_template('patients/detail.html', patient=patient, visits=visits, teeth=teeth)


# — Doctors —
@app.route('/doctors')
def doctors_list():
    doctors = Doctor.query.order_by(Doctor.FullName).all()
    return render_template('doctors/list.html', doctors=doctors)


# — Visits —
@app.route('/visits')
def visits_list():
    visits = Visit.query.order_by(Visit.VisitDateTime.desc()).all()
    return render_template('visits/list.html', visits=visits)


@app.route('/visits/new', methods=['GET', 'POST'])
def visit_create():
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(
            PatientID=form.patient_id.data,
            DoctorID=form.doctor_id.data,
            VisitDateTime=form.visit_datetime.data.strftime('%Y-%m-%d %H:%M:%S'),
            Complaint=form.complaint.data or None,
            Diagnosis=form.diagnosis.data or None,
            Status=form.status.data
        )
        db.session.add(visit)
        db.session.commit()
        flash("✅ Визит успешно записан!", "success")
        return redirect(url_for('visits_list'))
    return render_template('visits/create.html', form=form)


# — Services —
@app.route('/services')
def services_list():
    services = Service.query.order_by(Service.Category, Service.ServiceName).all()
    return render_template('services/list.html', services=services)


# — Tooth Chart —
@app.route('/teeth/<int:pid>')
def tooth_chart(pid):
    patient = Patient.query.get_or_404(pid)
    teeth_data = db.session.query(PatientTooth, Tooth).join(Tooth).filter(PatientTooth.PatientID == pid).all()
    # Создаём словарь: ToothNumber → (PatientTooth, Tooth)
    tooth_map = {pt_record.ToothNumber: (pt, pt_record) for pt, pt_record in teeth_data}
    return render_template('teeth/patient_card.html', patient=patient, tooth_map=tooth_map)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)