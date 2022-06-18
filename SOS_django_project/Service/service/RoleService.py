from Service.models import Role
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection
'''
It contains Role Buisness Logic

'''
class RoleService(BaseService):

    def search(self,params):
         print("Page No -->",params["pageno"])
         pageno =(params["pageno"]-1)*self.PageSize
         sql ="select * from sos_role where 1=1"
         val =params.get("name",None)
         if DataValidator.isNotNull(val):
             sql+=" and name ='"+val+"'"
         sql+=" limit %s,%s "
         cursor = connection.cursor()
         print("------------->",sql,pageno,self.PageSize)
         params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
         cursor.execute(sql,[pageno,self.PageSize])
         result =cursor.fetchall()
         columnName = ("id","name","description")
         res ={
                "data" : []
         }
         count = 0
         for x in result:
             params['MaxId'] = x[0]
             print({columnName[i] :x[i] for i,_ in enumerate(x)})
             res["data"].append({columnName[i] :  x[i] for i, _ in enumerate(x)})
         return res

    def get_model(self):
        return Role
             
