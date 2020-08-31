from flask_restful import Resource, reqparse,inputs
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.temperature import TemperatureModel
from models.student import StudentModel
import datetime


"""
The following resources contain endpoints that are protected by jwt,
one may need a valid access token, a valid fresh token or a valid token with authorized privilege 
to access each endpoint, details can be found in the README.md doc.  
"""


class Temperature(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('temperature',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
      #parser.add_argument('date',
                        #type=str,
                        #required=True,
                        #help="This field cannot be left blank!"
                        #)   
    #parser.add_argument('time',
                        #type=str,
                        #required=True,
                        #help="This field cannot be left blank!"
                        #)                                        
    #@jwt_required
    def get(self,college_id, rollno):
        temperatures = [temperature.json() for temperature in TemperatureModel.find_all_temp()]
        if temperatures:
            return {'temperatures': temperatures}, 200
        return {'message': 'Student not found'}, 404



    def post(self, college_id,rollno):
        stu=StudentModel.find_by_rollno(college_id,rollno)
        if not stu:
            return {"messgae":"student not found"}
        data = Temperature.parser.parse_args()
        #temperature = TemperatureModel(college_id,rollno, **data)
        
        if stu.password==data['password']:
            data = Temperature.parser.parse_args()
            temperature = TemperatureModel(college_id,rollno, **data)

        

        #temperature = TemperatureModel(college_id,rollno, **data)

        try:
            temperature.save_to_db()
        except:

            return {"message": 'Invalid Credentials'}, 500

        return temperature.json(), 201
        if not stu:
            return {"messgae":"student not found"}

    @jwt_required
    def delete(self, college_id,rollno):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        temperature = TemperatureModel.find_by_rollno(colllege_id,rollno)
        if temperature:
            temperature.delete_from_db()
            return {'message': 'Current temperature deleted.'}
        return {'message': 'Student not found.'}, 404

    def put(self,college_id,rollno):
        data = Temperature.parser.parse_args()

        temperature = TemperatureModel.find_by_rollno(college_id,rollno)

        if temperature:
            temperature.temperature = data['temperature']
        else:
            temperature = TemperatureModel(college_id,rollno, **data)

        temperature.save_to_db()

        return temperature.json()

class TemperatureList(Resource):
    #@jwt_optional
    def get(self,college_id,rollno):
        #user_id = get_jwt_identity()
        temperatures = [temperature.json() for temperature in TemperatureModel.find_all_temp(college_id,rollno)]
        #if user_id:
        return {'temperatures': temperatures}, 200
        #return {
        #    'temperatures': [temperature['rollno'] for temperature in temperatures],
        #    'message': 'More data available if you log in.'
        #}, 200
class TemperatureList_clg(Resource):
    #@jwt_optional
    def get(self,college_id):
        #user_id = get_jwt_identity()
        temperatures = [temperature.json() for temperature in TemperatureModel.find_by_id(college_id)]
        #if user_id:
        return {'temperatures': temperatures}, 200

