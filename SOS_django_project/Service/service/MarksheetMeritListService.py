from Service.models import Marksheet
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''
It contains Role business logics.   
'''
class MarksheetMeritListService(BaseService):
    def search(self,params):
        sql= "select id, rollNumber, name, physics, chemistry, maths, physics+chemistry+maths as total, (physics+chemistry+maths)/3 as percentage from sos_marksheet where 1=1 order by rollNumber, name, physics, chemistry, maths, total, percentage  desc, (physics>33), (chemistry>33), (maths>33) limit 10;" 
        cursor = connection.cursor()
        cursor.execute(sql)
        params['index'] = ((params['pageno']-1)* self.PageSize)  + 1
        result = cursor.fetchall()
        print("------service result",result)
        columnName = ("id","rollNumber","name","physics","chemistry","maths","total","percentage")
        res ={
            "data":[]
        }
        for x in result:
            params["MaxID"] =x[0]
            res['data'].append({columnName[i] :  x[i] for i, _ in enumerate(x)})
            print(res)
        return res

    def get_model(self):
        return Marksheet

