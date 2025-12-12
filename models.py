# models.py
from database import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'Patients'
    PatientID = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(100), nullable=False)
    BirthDate = db.Column(db.String(10), nullable=False)  # 'YYYY-MM-DD'
    Phone = db.Column(db.String(20), nullable=False, unique=True)
    Email = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    RegDate = db.Column(db.String(19), nullable=False, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    visits = db.relationship('Visit', back_populates='patient', cascade='all, delete-orphan')
    teeth_records = db.relationship('PatientTooth', back_populates='patient', cascade='all, delete-orphan')
    treatment_plans = db.relationship('TreatmentPlan', back_populates='patient', cascade='all, delete-orphan')

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    DoctorID = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(100), nullable=False)
    Specialization = db.Column(db.String(50), nullable=False)
    Cabinet = db.Column(db.Integer, nullable=False)
    Experience = db.Column(db.Integer, nullable=False)

    visits = db.relationship('Visit', back_populates='doctor')

class Tooth(db.Model):
    __tablename__ = 'Teeth'
    ToothID = db.Column(db.Integer, primary_key=True)
    ToothNumber = db.Column(db.Integer, nullable=False, unique=True)
    ToothName = db.Column(db.String(100), nullable=False)
    ToothType = db.Column(db.String(20), nullable=False)  # 'permanent' / 'deciduous'

    patient_teeth = db.relationship('PatientTooth', back_populates='tooth')

class PatientTooth(db.Model):
    __tablename__ = 'PatientTeeth'
    RecordID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('Patients.PatientID', ondelete='CASCADE'), nullable=False)
    ToothID = db.Column(db.Integer, db.ForeignKey('Teeth.ToothID'), nullable=False)
    Status = db.Column(db.String(20), nullable=False)  # healthy, caries, filled, crown, missing, implant
    LastUpdate = db.Column(db.String(19), nullable=False, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    Notes = db.Column(db.Text)

    patient = db.relationship('Patient', back_populates='teeth_records')
    tooth = db.relationship('Tooth', back_populates='patient_teeth')

class Visit(db.Model):
    __tablename__ = 'Visits'
    VisitID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('Patients.PatientID'), nullable=False)
    DoctorID = db.Column(db.Integer, db.ForeignKey('Doctors.DoctorID'), nullable=False)
    VisitDateTime = db.Column(db.String(19), nullable=False)  # 'YYYY-MM-DD HH:MM:SS'
    Complaint = db.Column(db.Text)
    Diagnosis = db.Column(db.Text)
    Status = db.Column(db.String(20), nullable=False, default='scheduled')  # scheduled, completed, cancelled

    patient = db.relationship('Patient', back_populates='visits')
    doctor = db.relationship('Doctor', back_populates='visits')
    services = db.relationship('VisitService', back_populates='visit', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='visit', cascade='all, delete-orphan')
    plan_stages = db.relationship('PlanStage', back_populates='visit')

class Service(db.Model):
    __tablename__ = 'Services'
    ServiceID = db.Column(db.Integer, primary_key=True)
    ServiceName = db.Column(db.String(100), nullable=False, unique=True)
    Category = db.Column(db.String(50), nullable=False)
    PriceCents = db.Column(db.Integer, nullable=False)  # in cents (e.g., 15000 = 150.00)
    DurationMin = db.Column(db.Integer)

    visit_services = db.relationship('VisitService', back_populates='service')

class VisitService(db.Model):
    __tablename__ = 'VisitServices'
    VisitID = db.Column(db.Integer, db.ForeignKey('Visits.VisitID', ondelete='CASCADE'), primary_key=True)
    ServiceID = db.Column(db.Integer, db.ForeignKey('Services.ServiceID'), primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    PriceAtTimeCents = db.Column(db.Integer, nullable=False)
    TotalCents = db.Column(db.Integer, nullable=False)  # computed as Qty * PriceAtTimeCents

    visit = db.relationship('Visit', back_populates='services')
    service = db.relationship('Service', back_populates='visit_services')

class TreatmentPlan(db.Model):
    __tablename__ = 'TreatmentPlans'
    PlanID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('Patients.PatientID'), nullable=False)
    StartDate = db.Column(db.String(10), nullable=False, default=lambda: datetime.now().strftime('%Y-%m-%d'))
    Status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, cancelled
    Description = db.Column(db.Text)

    patient = db.relationship('Patient', back_populates='treatment_plans')
    stages = db.relationship('PlanStage', back_populates='plan', cascade='all, delete-orphan')

class PlanStage(db.Model):
    __tablename__ = 'PlanStages'
    StageID = db.Column(db.Integer, primary_key=True)
    PlanID = db.Column(db.Integer, db.ForeignKey('TreatmentPlans.PlanID', ondelete='CASCADE'), nullable=False)
    StageName = db.Column(db.String(100), nullable=False)
    DueDate = db.Column(db.String(10))
    Status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, skipped
    VisitID = db.Column(db.Integer, db.ForeignKey('Visits.VisitID'))
    OrderNum = db.Column(db.Integer, nullable=False)

    plan = db.relationship('TreatmentPlan', back_populates='stages')
    visit = db.relationship('Visit', back_populates='plan_stages')

class Payment(db.Model):
    __tablename__ = 'Payments'
    PaymentID = db.Column(db.Integer, primary_key=True)
    VisitID = db.Column(db.Integer, db.ForeignKey('Visits.VisitID'), nullable=False)
    AmountCents = db.Column(db.Integer, nullable=False)
    PaymentDate = db.Column(db.String(19), nullable=False, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    Method = db.Column(db.String(20), nullable=False)  # cash, card, transfer
    IsPaid = db.Column(db.Boolean, nullable=False, default=True)

    visit = db.relationship('Visit', back_populates='payments')