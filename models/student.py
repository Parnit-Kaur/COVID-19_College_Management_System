from db import db
import random
import string


class StudentModel(db.Model):
    __tablename__ = 'students'

    rollno = db.Column(db.Integer)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), primary_key=True)
    password=db.Column(db.String(80)) 
    #clg_password=db.Column(db.String(80))


    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))
    college = db.relationship('CollegeModel')

    def __init__(self, college_id,rollno,name, email,password,clg_password):
        self.college_id = college_id
        self.rollno=rollno
        self.name = name
        self.email = email
        self.password=self.gen_password()
        self.clg_password=clg_password

    @classmethod
    def gen_password(self):
        letters_and_digits =  string.digits
        #string.ascii_letters.upper()# +
        password = ''.join((random.choice(letters_and_digits) for i in range(4)))
        return password         
        

    def json(self):
        return {'rollno': self.rollno,'name': self.name, 'email': self.email, 'password': self.password}

    @classmethod
    def find_by_rollno(cls,college_id,rollno):
        return cls.query.filter_by(rollno=rollno,college_id=college_id).first()

    
        
    @classmethod
    def find_all(cls,college_id):
        return cls.query.filter_by(college_id=college_id).all()
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
