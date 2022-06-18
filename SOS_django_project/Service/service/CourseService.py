


from Service.models import Course
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''
It contains Course business logics.   
'''
class CourseService(BaseService):
    def get_model(self):
        return Course
   
    def search(self,params):
        pageno = (params["pageno"]-1)*self.PageSize
        sql="select * from sos_course where 1=1"
        val = params.get("courseName", None)
        if DataValidator.isNotNull(val):
            sql+=" and courseName = '"+val+"' "
        sql+=" limit %s,%s" 
        cursor = connection.cursor()
        params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
        cursor.execute(sql,[pageno,self.PageSize])
        result=cursor.fetchall()
        columnName=("id","courseName","courseDescription","courseDuration")
        res={
            "data":[]
        }
        count=0
        for x in result:
            params['MaxId'] = x[0]
            print({columnName[i] :  x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

    
