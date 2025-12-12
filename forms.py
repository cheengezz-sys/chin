# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateTimeLocalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange, Optional
from models import Patient, Doctor, Service
from database import db

class PatientForm(FlaskForm):
    full_name = StringField('ФИО', validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=5, max=100, message="От 5 до 100 символов")
    ])
    birth_date = StringField('Дата рождения', validators=[
        DataRequired(),
        Regexp(r'^\d{4}-\d{2}-\d{2}$', message="Формат: ГГГГ-ММ-ДД")
    ])
    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+7\d{10}$', message="Формат: +77011234567")
    ])
    email = StringField('Email', validators=[Optional(), Email()])
    address = StringField('Адрес', validators=[Length(max=200)])
    submit = SubmitField('Добавить пациента')

class VisitForm(FlaskForm):
    patient_id = SelectField('Пациент', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Врач', coerce=int, validators=[DataRequired()])
    visit_datetime = DateTimeLocalField('Дата и время визита', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    complaint = TextAreaField('Жалобы', validators=[Length(max=500)])
    diagnosis = TextAreaField('Диагноз', validators=[Length(max=500)])
    status = SelectField('Статус', choices=[
        ('scheduled', 'Запланирован'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён')
    ], default='scheduled')
    submit = SubmitField('Записать на приём')

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        self.patient_id.choices = [(p.PatientID, p.FullName) for p in Patient.query.order_by(Patient.FullName).all()]
        self.doctor_id.choices = [(d.DoctorID, f"{d.FullName} ({d.Specialization})") for d in Doctor.query.order_by(Doctor.FullName).all()]