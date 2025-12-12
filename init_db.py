# init_db.py
from app import app, db
from models import Patient, Doctor, Tooth, PatientTooth, Visit, Service, VisitService, TreatmentPlan, PlanStage, Payment
from datetime import datetime, timedelta

def create_teeth():
    if Tooth.query.count() == 0:
        # Permanent teeth 1–32 (FDI notation)
        permanent = [
            (1, "18 — правый верхний 3-й моляр", "permanent"),
            (2, "17 — правый верхний 2-й моляр", "permanent"),
            (3, "16 — правый верхний 1-й моляр", "permanent"),
            (4, "15 — правый верхний 2-й премоляр", "permanent"),
            (5, "14 — правый верхний 1-й премоляр", "permanent"),
            (6, "13 — правый верхний клык", "permanent"),
            (7, "12 — правый верхний боковой резец", "permanent"),
            (8, "11 — правый верхний центральный резец", "permanent"),
            (9, "21 — левый верхний центральный резец", "permanent"),
            (10, "22 — левый верхний боковой резец", "permanent"),
            (11, "23 — левый верхний клык", "permanent"),
            (12, "24 — левый верхний 1-й премоляр", "permanent"),
            (13, "25 — левый верхний 2-й премоляр", "permanent"),
            (14, "26 — левый верхний 1-й моляр", "permanent"),
            (15, "27 — левый верхний 2-й моляр", "permanent"),
            (16, "28 — левый верхний 3-й моляр", "permanent"),
            (17, "48 — правый нижний 3-й моляр", "permanent"),
            (18, "47 — правый нижний 2-й моляр", "permanent"),
            (19, "46 — правый нижний 1-й моляр", "permanent"),
            (20, "45 — правый нижний 2-й премоляр", "permanent"),
            (21, "44 — правый нижний 1-й премоляр", "permanent"),
            (22, "43 — правый нижний клык", "permanent"),
            (23, "42 — правый нижний боковой резец", "permanent"),
            (24, "41 — правый нижний центральный резец", "permanent"),
            (25, "31 — левый нижний центральный резец", "permanent"),
            (26, "32 — левый нижний боковой резец", "permanent"),
            (27, "33 — левый нижний клык", "permanent"),
            (28, "34 — левый нижний 1-й премоляр", "permanent"),
            (29, "35 — левый нижний 2-й премоляр", "permanent"),
            (30, "36 — левый нижний 1-й моляр", "permanent"),
            (31, "37 — левый нижний 2-й моляр", "permanent"),
            (32, "38 — левый нижний 3-й моляр", "permanent"),
        ]
        for num, name, ttype in permanent:
            db.session.add(Tooth(ToothNumber=num, ToothName=name, ToothType=ttype))
        db.session.commit()

def add_doctors():
    doctors = [
        ("Иванов Иван Иванович", "Терапевт", 101, 10),
        ("Петрова Анна Сергеевна", "Ортодонт", 102, 7),
        ("Сидоров Дмитрий Владимирович", "Хирург", 103, 12),
        ("Жакупова Айгерим Канатовна", "Имплантолог", 104, 8),
        ("Нурпеисов Ерлан Азаматович", "Гигиенист", 105, 5),
    ]
    for name, spec, cab, exp in doctors:
        if not Doctor.query.filter_by(FullName=name).first():
            db.session.add(Doctor(FullName=name, Specialization=spec, Cabinet=cab, Experience=exp))
    db.session.commit()

def add_patients():
    patients = [
        ("Смирнов Алексей", "1990-05-12", "+77011234567", "smirnov@example.com", "г. Астана, ул. Абая 10"),
        ("Кузнецова Мария", "1985-11-30", "+77029876543", "kuzn@example.com", "г. Астана, пр. Нуркелди 15"),
        ("Ахметов Руслан", "1978-03-22", "+77071112233", None, "г. Алматы, ул. Жандосова 45"),
        ("Ержанова Гульнара", "2001-08-14", "+77054445566", "gulnara@mail.kz", "г. Шымкент, ул. Толе би 7"),
        ("Темирханов Али", "1995-12-01", "+77778889900", "ali.t@example.com", "г. Астана, мкр. Самал 3"),
        ("Оразбаева Асем", "1992-02-18", "+77089998877", "asem_o@yandex.kz", "г. Караганда, ул. Сатпаева 33"),
        ("Бекетов Нурлан", "1988-07-05", "+77012341234", None, "г. Актау, ул. Мангилау 21"),
        ("Мухамеджанова Жанар", "2000-09-30", "+77023452345", "janar.m@gmail.com", "г. Астана, ЖК Green City"),
        ("Кенжебаев Данияр", "1975-04-11", "+77771234567", "daniyar_k@mail.kz", "г. Павлодар, ул. Ломова 8"),
        ("Жаксыбекова Салтанат", "1997-06-25", "+77087654321", "sultanat_j@example.kz", "г. Астана, ул. Манас 50"),
    ]
    for full_name, birth, phone, email, addr in patients:
        if not Patient.query.filter_by(Phone=phone).first():
            db.session.add(Patient(
                FullName=full_name,
                BirthDate=birth,
                Phone=phone,
                Email=email,
                Address=addr
            ))
    db.session.commit()

def add_services():
    services = [
        ("Консультация врача", "Диагностика", 3000, 15),
        ("Осмотр + КЛКТ", "Диагностика", 12000, 30),
        ("Пломбирование одного зуба", "Терапия", 25000, 45),
        ("Лечение пульпита", "Терапия", 45000, 60),
        ("Удаление зуба простое", "Хирургия", 15000, 30),
        ("Удаление зуба сложное (ретинированный)", "Хирургия", 35000, 60),
        ("Имплантация (включая установку импланта)", "Ортопедия", 250000, 90),
        ("Установка абатмента", "Ортопедия", 50000, 30),
        ("Установка циркониевой коронки", "Ортопедия", 120000, 45),
        ("Отбеливание зубов (ZOOM)", "Эстетика", 85000, 90),
        ("Профессиональная гигиена (Air Flow + полировка)", "Гигиена", 20000, 60),
        ("Установка брекет-системы (металл)", "Ортодонтия", 180000, 120),
    ]
    for name, cat, price, dur in services:
        if not Service.query.filter_by(ServiceName=name).first():
            db.session.add(Service(ServiceName=name, Category=cat, PriceCents=price*100, DurationMin=dur))
    db.session.commit()

def add_detailed_patient_teeth():
    patients = Patient.query.limit(3).all()
    teeth = Tooth.query.filter_by(ToothType='permanent').order_by(Tooth.ToothNumber).all()
    statuses = ['healthy', 'caries', 'filled', 'crown', 'missing', 'implant']

    for i, p in enumerate(patients):
        for j, tooth in enumerate(teeth):
            # Случайный статус, но для демонстрации — разные
            status = statuses[(i + j) % len(statuses)]
            notes = {
                'caries': f"Кариес на {tooth.ToothNumber}",
                'filled': f"Пломба на {tooth.ToothNumber} (2025)",
                'crown': f"Циркониевая коронка на {tooth.ToothNumber}",
                'missing': f"Удалён в 2020",
                'implant': f"Имплант на месте {tooth.ToothNumber}",
                'healthy': ""
            }.get(status, "")
            pt = PatientTooth(
                PatientID=p.PatientID,
                ToothID=tooth.ToothID,
                Status=status,
                Notes=notes
            )
            db.session.add(pt)
    db.session.commit()

def add_visits_and_related():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    services = Service.query.all()

    now = datetime(2025, 12, 10, 9, 0)
    for i in range(25):
        p = patients[i % len(patients)]
        d = doctors[i % len(doctors)]
        dt = now + timedelta(days=i//5, hours=(i*2) % 8 + 9)
        status = ['completed', 'scheduled', 'cancelled'][i % 3]

        v = Visit(
            PatientID=p.PatientID,
            DoctorID=d.DoctorID,
            VisitDateTime=dt.strftime('%Y-%m-%d %H:%M:%S'),
            Complaint=f"Жалоба {i+1}: боль/эстетика/профилактика",
            Diagnosis=f"Диагноз {i+1}",
            Status=status
        )
        db.session.add(v)
        db.session.flush()  # Получить VisitID

        # Добавим 1-3 услуги
        selected_services = services[(i)%len(services): (i)%len(services)+2]
        total = 0
        for svc in selected_services[:2]:
            qty = 1
            price = svc.PriceCents
            vs = VisitService(
                VisitID=v.VisitID,
                ServiceID=svc.ServiceID,
                Quantity=qty,
                PriceAtTimeCents=price,
                TotalCents=qty * price
            )
            db.session.add(vs)
            total += qty * price

        # Платёж: 80% случаев — оплачено
        if status == 'completed' and i % 5 != 0:
            # Полная оплата
            db.session.add(Payment(
                VisitID=v.VisitID,
                AmountCents=total,
                Method=['cash', 'card', 'transfer'][i % 3],
                IsPaid=True
            ))
        elif status == 'completed' and i % 5 == 0:
            # Частичная оплата
            db.session.add(Payment(
                VisitID=v.VisitID,
                AmountCents=int(total * 0.6),
                Method='card',
                IsPaid=True
            ))
            db.session.add(Payment(
                VisitID=v.VisitID,
                AmountCents=int(total * 0.4),
                Method='transfer',
                IsPaid=True
            ))

    db.session.commit()

def add_treatment_plans():
    patients = Patient.query.limit(6).all()
    services = Service.query.filter(Service.ServiceName.in_([
        "Удаление зуба простое", "Имплантация (включая установку импланта)",
        "Установка абатмента", "Установка циркониевой коронки"
    ])).all()

    for i, p in enumerate(patients):
        plan = TreatmentPlan(
            PatientID=p.PatientID,
            Description=f"Комплексное восстановление зуба у пациента {p.FullName}",
            Status='active' if i < 4 else 'completed'
        )
        db.session.add(plan)
        db.session.flush()

        stages = [
            ("Удаление зуба 16", "2025-12-12", services[0]),
            ("Имплантация", "2026-02-01", services[1]),
            ("Установка абатмента", "2026-04-15", services[2]),
            ("Установка коронки", "2026-06-10", services[3]),
        ]
        for j, (name, due, svc) in enumerate(stages):
            status = 'completed' if i < 2 and j < 2 else 'pending'
            stage = PlanStage(
                PlanID=plan.PlanID,
                StageName=name,
                DueDate=due,
                Status=status,
                OrderNum=j+1
            )
            db.session.add(stage)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Очистка (для повторного запуска)
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        print("🔁 Создаём справочник зубов...")
        create_teeth()
        print("👨‍⚕️ Добавляем врачей...")
        add_doctors()
        print("🧑 Добавляем пациентов...")
        add_patients()
        print("📋 Добавляем услуги...")
        add_services()
        print("🦷 Заполняем зубные карты...")
        add_detailed_patient_teeth()
        print("📅 Добавляем визиты, услуги и платежи...")
        add_visits_and_related()
        print("📋 Добавляем планы лечения...")
        add_treatment_plans()

        print(f"\n✅ База данных инициализирована!")
        print(f"   Пациентов: {Patient.query.count()}")
        print(f"   Врачей: {Doctor.query.count()}")
        print(f"   Услуг: {Service.query.count()}")
        print(f"   Визитов: {Visit.query.count()}")
        print(f"   Платежей: {Payment.query.count()}")
        print(f"   Записей в зубных картах: {PatientTooth.query.count()}")