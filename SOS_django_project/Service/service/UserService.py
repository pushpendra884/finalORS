from Service.models import User
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''It contains user buisness logic'''
class UserService(BaseService):
    def authenticate(self,Params):
        userList = self.search2(Params)
        if (userList.count() == 1):
            return userList[0]
        else:
            return None


    def search2(self,params):
        q = self.get_model().objects.filter()

        val = params.get("login_id",None)
        if (DataValidator.isNotNull(val)):
            q = q.filter(login_id = val)
            print("---Login id will search with model---",val)

        val = params.get("password",None)
        if (DataValidator.isNotNull(val)):
            q = q.filter(password = val)
            print("---Password will search with model---",val)


        return q

    def search(self,params):
        pageno = (params["pageno"]-1)*self.PageSize
        sql ="select * from sos_user where 1 = 1"
        val = params.get("login_id",None)
        if DataValidator.isNotNull(val):
            sql+=" and login_id = '"+val+"' "
        sql+= " limit %s,%s"
        cursor = connection.cursor()
        print("-------->",sql,pageno,self.PageSize,val)
        params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
        print("ttttttttttt",params["index"])
        cursor.execute(sql,[pageno,self.PageSize])
        result =cursor.fetchall()
        columnName =("id","firstName","lastName","login_id","password","confirmpassword","dob","address","gender","mobilenumber","role_Id","role_Name")
        res ={
            "data":[]
        }
        count = 0
        for x in result:
            params['MaxId'] = x[0]
            res["data"].append({columnName[i] : x[i] for i, _  in enumerate(x)})
        return res


    def get_login_id(self,login_id):
        self.get_model.objects.all()

    def get_model(self):
        return User

 
        
        
