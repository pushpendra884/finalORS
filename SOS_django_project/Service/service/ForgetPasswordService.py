from Service.models import User
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService

'''
It contains Role Buisness Logic
'''
class ForgetPasswordService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("login_id",None)
        if (DataValidator.isNotNull(val)):
            q = q.filter( login = val)
        return q

    def get_model(self):
        return User