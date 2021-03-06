from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from flask_jwt_extended import jwt_refresh_token_required,get_jwt_identity
from smartexpenses.Model.expense import Expense
from smartexpenses.Model.user import User
from smartexpenses.Model.profile import Profile

parser = reqparse.RequestParser()
parser.add_argument('color', help = 'This field cannot be blank', required = True)
parser.add_argument('notifications', help = 'This field cannot be blank', required = True)
parser.add_argument('profile_image', help = 'This field cannot be blank', required = True)
parser.add_argument('num_latest_spendings', help = 'This field cannot be blank', required = True)



class GetProfile(Resource):
    @jwt_refresh_token_required
    def get(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            return {
                'profile' : Profile.return_profile_by_user_id(user_id),
                'status' : 0
            }
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

class UpdateProfile(Resource):
    @jwt_refresh_token_required
    def put(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        data = parser.parse_args()
        try:
            Profile.update_profile_by_user_id(user_id,data)
            return{
                # 'Profile':Profile.return_profile_by_user_id(user_id),
                'message':'Your profile was updated',
                'status':0
            },200
        except Exception as error:
            return{
                'message':repr(error),
                'status':1
            },500
