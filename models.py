import peewee
from database import db

class Student(peewee.Model):
    name = peewee.CharField()
    address = peewee.CharField()
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()


    class Meta:
        database = db

