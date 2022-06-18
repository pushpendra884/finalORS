



from Service.models import Faculty
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''
It contains Student business logics.
'''
class AddFacultyService(BaseService):
   def get_model(self):
        return Faculty

   def preload(self,params):
       pass
   
   def search(self,params):
      print("Page no -->",params["pageno"])
      pageno = (params["pageno"]-1)*self.PageSize
      sql="select * from sos_faculty where 1=1"
      val = params.get("firstName", None)
      if DataValidator.isNotNull(val):
         sql+=" and firstName = '"+val+"' "
      sql+=" limit %s,%s" 
      cursor = connection.cursor()
      params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
      print("------------->",sql,params["pageno"],self.PageSize)
      cursor.execute(sql,[pageno,self.PageSize])
      result=cursor.fetchall()
      columnName=("id","firstName","lastName","email","password","address","gender","dob","college_ID","collegeName","subject_ID","subjectName","course_ID","courseName")
      res={
         "data":[]
      }
      count=0
      for x in result:
         params["MaxId"] = x[0]
         print({columnName[i] :  x[i] for i, _ in enumerate(x)})
         res["data"].append({columnName[i] :  x[i] for i, _ in enumerate(x)})            
      return res
    
    
    