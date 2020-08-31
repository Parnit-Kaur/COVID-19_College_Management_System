from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.student import StudentModel
from models.college import CollegeModel


"""
The following resources contain endpoints that are protected by jwt,
one may need a valid access token, a valid fresh token or a valid token with authorized privilege 
to access each endpoint, details can be found in the README.md doc.  
"""


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('clg_password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        )
    
    @jwt_required
    def get(self,college_id, rollno):
        student = StudentModel.find_by_rollno(college_id,rollno)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404

    def post(self, college_id,rollno):
         
        data = Student.parser.parse_args()
            
        clg=CollegeModel.find_by_id(college_id)
        if clg.password==data['clg_password']:
            
            if StudentModel.find_by_rollno(college_id,rollno):
                return {'message': "An student with rollno '{}' already exists.".format(rollno)}, 400
            
            data = Student.parser.parse_args()

            student = StudentModel(college_id,rollno, **data)

            try:
                student.save_to_db()
            except:
                return {"message": "An error occurred inserting the student."}, 500

            return student.json(), 201
        else:
            return {"message":"Please enter the correct password!"}   
    
    
    def delete(self, college_id,rollno):
        data = Student.parser.parse_args()
        clg=CollegeModel.find_by_id(college_id)
        if clg.password==data['clg_password']:
            student = StudentModel.find_by_rollno(college_id,rollno)
            if student:
                student.delete_from_db()
                return {'message': 'Student deleted.'}
            return {'message': 'Student not found.'}, 404

    def put(self,college_id,rollno):
        data = Student.parser.parse_args()
        clg=CollegeModel.find_by_id(college_id)
        if clg.password==data['clg_password']:

            student = StudentModel.find_by_rollno(college_id,rollno)

            if student:
                student.name = data['name']
                student.email = data['email']
            else:
                student = StudentModel(college_id,rollno, **data)

            student.save_to_db()

            return student.json()
        else:
           return {"message":"Please enter correct password"}    

class StudentList(Resource):
    #@jwt_required
    def get(self,college_id):
        students = [student.json() for student in StudentModel.find_all(college_id)]
        #if user_id:
        return {'students': students}, 200
        #return {
        #    'students': [student['rollno'] for student in students],
        #    'message': 'More data available if you log in.'
        #}, 200

