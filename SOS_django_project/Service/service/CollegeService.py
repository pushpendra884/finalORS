from Service.models import College
from Service.utility.DataValidator import DataValidator
from .Base_serviece import BaseService
from django.db import connection

'''
It contains Role business logic's.   
'''


class CollegeService(BaseService):
    
    def get_model(self):
        return College
    def search(self, params):
        pageno = (params["pageno"] - 1) * self.PageSize
        sql = "select * from sos_college where 1=1"
        val = params.get("collegeName", None)
        if DataValidator.isNotNull(val):
            sql+= " and collegeName = '" + val +"' "  
        sql+= " limit %s,%s"
        cursor = connection.cursor()
        print("-----------",sql,[pageno,self.PageSize])
        params["index"] = ((params["pageno"]-1)*self.PageSize) + 1
        cursor.execute(sql, [pageno,self.PageSize])
        resultt = cursor.fetchall()
        columnName = ("id", "collegeName", "collegeAddress", "collegeState", "collegeCity", "collegePhoneNumber")
        res = {
            "data": []
        }
        count = 0
        for x in resultt:
            params['MaxId'] = x[0]
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res
 