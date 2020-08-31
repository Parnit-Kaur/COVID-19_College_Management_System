from db import db


class CollegeModel(db.Model):
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password=db.Column(db.String(80))

    students = db.relationship('StudentModel', lazy='dynamic')
    temperatures = db.relationship('TemperatureModel', lazy='dynamic')

    def __init__(self, name,email,password):
        self.name = name
        self.email=email
        self.password=password
 
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email':self.email,
            'students': [student.json() for student in self.students.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()    

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
