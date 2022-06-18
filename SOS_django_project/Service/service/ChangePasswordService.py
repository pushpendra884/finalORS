from collections import UserList
from Service.models import User
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService

'''
It contain User Buisness logics.
'''
class ChangePasswordService(BaseService):

    def authenticate(self,params):
        userList = self.search(params)
        if (UserList.count()>0):
            print("----->", userList[0].login)
            return UserList[0]

        else:
            return None
    
    def get_model(self):
        return User
            
