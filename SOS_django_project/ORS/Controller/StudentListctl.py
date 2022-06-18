from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.forms import StudentForm
from Service.models import Student
from Service.service.StudentService import StudentService

class StudentListctl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["firstName"]=requestForm.get("firstName",None)
        self.form["lastName"]=requestForm.get("lastName",None)
        self.form["dob"]=requestForm.get("dob",None)
        self.form["mobileNumber"]=requestForm.get("mobileNumber",None)
        self.form["email"]=requestForm.get("email",None)
        self.form["college_ID"]=requestForm.get("college_ID",None)
        self.form["collegeName"]=requestForm.get("collegeName",None)
        self.form["ids"]=requestForm.getlist("ids",None)

    def display(self, request, params={}):
        StudentListctl.count = self.form['pageno']
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form['LastId'] = Student.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def next(self,request,params={}):
        StudentListctl.count +=1
        self.form["pageno"] = StudentListctl.count
        self.form['LastId'] = Student.objects.last().id

        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def previous (self,request,params={}):
        StudentListctl.count-=1
        self.form["pageno"] = StudentListctl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.form['LastId'] = Student.objects.last().id
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list ==[]:
            self.form['msg'] = "NO RECORD FOUND"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res 

    def get_template(self):
        return "StudentList.html"

    #  Service of Marksheet

    def get_service(self):
        return StudentService()
    def deleteRecord(self,request,params={}):
        self.form["pageno"]=StudentListctl.count
        if(bool(self.form["ids"])==False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            record = self.get_service().search(self.form)
            self.page_list=record["data"]
            self.form['LastId'] = Student.objects.last().id

            return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list=record["data"]

                id=int(ids)
                if( id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        record = self.get_service().search(self.form)
                        self.page_list=record["data"]
                        self.form["pageno"]=1
                        self.form["error"] = False
                        self.form["message"] = "DATA IS SUCCESSFULLY DELETED"
                        print("ppppppp-->",self.page_list)
                        res= render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res= render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res
    