from flask_restful import Resource,reqparse
from models.college import CollegeModel


class College(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannotbe left blank!"
                        )
    @classmethod
    def get(cls, name):
        college = CollegeModel.find_by_name(name)
        if college:
            return college.json()
        return {'message': 'College not found'}, 404

    @classmethod
    def post(cls, name):
        if CollegeModel.find_by_name(name):
            return {'message': "A college with name '{}' already exists.".format(name)}, 400

        data = College.parser.parse_args()

        college = CollegeModel(name,**data)

        try:
            college.save_to_db()
        except:
            return {"message": "An error occurred creating the college."}, 500

        return college.json(), 201

    @classmethod
    def delete(cls, name):
        college = CollegeModel.find_by_name(name)
        if college:
            college.delete_from_db()

        return {'message': 'College deleted'}


class CollegeList(Resource):
    @classmethod
    def get(cls):
        return {'colleges': [college.json() for college in CollegeModel.find_all()]}
