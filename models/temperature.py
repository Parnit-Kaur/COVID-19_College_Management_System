from db import db
import datetime
import uuid


class TemperatureModel(db.Model):
    __tablename__ = 'temperatures'
    
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    rollno = db.Column(db.Integer)
    password=db.Column(db.String(80))
    temperature=db.Column(db.Float)
    date_time=db.Column(db.DateTime) 
    allow_entry=db.Column(db.Boolean)
    #date_time=db.Column(db.Integer) 

    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))
    college = db.relationship('CollegeModel')

    #rollno = db.Column(db.Integer, db.ForeignKey('students.rollno'),primary_key=True)
    #student = db.relationship('StudentModel')

    def __init__(self, college_id,rollno,password,temperature): 
        #self.id=
        self.college_id = college_id
        self.rollno=rollno
        self.password=password
        self.temperature=temperature
        self.date_time=datetime.datetime.now()
        self.allow_entry=self.check(self.temperature)
        #self.time=time
    



    @classmethod
    def check(self,temperature):
        if temperature>98.9:
            return False
        else:
            return True
       
    def json(self):
        return {'college_id':self.college_id,'rollno': self.rollno,'temperature':self.temperature,'date_time':self.date_time.strftime("%Y-%m-%d %H:%M:%S"),'allow entry':self.check(self.temperature)}
      
                    

    @classmethod
    def find_by_rollno(cls,college_id,rollno):
        return cls.query.filter_by(rollno=rollno,college_id=college_id).first()
    
    @classmethod
    def find_by_id(cls,college_id):
        return cls.query.filter_by(college_id=college_id).all()       
    #@classmethod
    #def find_by_pass(cls,college_id,rollno,password):
    #    return cls.query.filter_by(rollno=rollno,college_id=college_id,password=password).first()
    
    @classmethod
    def find_all_temp(cls,college_id,rollno):
        return cls.query.filter_by(college_id=college_id,rollno=rollno).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
