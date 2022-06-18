from re import I
from Service.models import Student
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''
It contains Student Buisness Logic
'''

class StudentService(BaseService):
    def search(self,params):
        print("page no-->",params["pageno"])
        pageno = (params["pageno"]-1)*self.PageSize
        sql = "select * from sos_student where 1 = 1 "
        val = params.get("firstName",None)
        if DataValidator.isNotNull(val):
            sql+=" and firstName = '"+val+"' "
        sql+=" limit %s,%s"
        cursor = connection.cursor()
        print("-------->",sql,params["pageno"],self.PageSize)
        params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
        cursor.execute(sql,[pageno,self.PageSize])
        result = cursor.fetchall()
        columnName = ("id","firstName","lastName","dob","mobileNumber","email","college_ID","collegeName")
        res ={
            "data":[]
        }
        count = 0
        for x in result:
            params["MaxId"] = x[0]
            print ({columnName[i] : x[i] for i , _ in enumerate(x)})
            res["data"].append({columnName[i] : x[i] for i , _ in enumerate(x)})
        return res

    def get_model(self):
        return Student


