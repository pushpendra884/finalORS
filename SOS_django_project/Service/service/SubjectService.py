


from Service.models import Subject
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection
'''
It contains Student business logics.   
'''
class SubjectService(BaseService):
    
    def search(self,params):
        print("Page no -->",params["pageno"])
        pageno = (params["pageno"]-1)*self.PageSize
        sql="select * from sos_subject where 1=1"
        val = params.get("subjectName", None)
        if DataValidator.isNotNull(val):
            sql+=" and subjectName = '"+val+"' "
        sql+=" limit %s,%s" 
        cursor = connection.cursor()
        print("------------->",sql,params["pageno"],self.PageSize)
        params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
        cursor.execute(sql,[pageno,self.PageSize])
        result=cursor.fetchall()
        columnName=("id","subjectName","subjectDescription","dob","course_ID","courseName")
        res={
            "data":[]
        }
        count=0
        for x in result:
            params["MaxId"] = x[0]
            print({columnName[i] :  x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i] :  x[i] for i, _ in enumerate(x)})            
        return res  


        

    def get_model(self):
        return Subject
