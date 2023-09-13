import models, schemas

def create_student(student: schemas.StudentCreate):
    fake_hashed_password = student.password + "temporary_hash"
    db_student = models.Student(name = student.name, address = student.address, email = student.email, hashed_password = fake_hashed_password)
    db_student.save()
    return db_student

def get_student_by_id(student_id: int):
    return models.Student.filter(models.Student.id == student_id).first()

def get_student_by_email(email: str):
    return models.Student.filter(models.Student.email == email).first()

def get_students(skip: int = 0, limit: int = 100):
    return list(models.Student.select().offset(skip).limit(limit))

