from django.http import HttpResponse

from ORS.Controller.StudentListctl import StudentListctl
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.forms import RoleForm, UserForm
from Service.models import User, Role
from Service.service.RoleService import RoleService

class RoleListctl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name",None)
        self.form["description"] = requestForm.get("description",None)
        self.form["ids"] = requestForm.getlist("ids",None)

    def display(self, request, params={}):
        RoleListctl.count = self.form['pageno']
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form['LastId'] = Role.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def next(self,request,params={}):
        RoleListctl.count+=1
        self.form["pageno"] = RoleListctl.count 
        self.form['LastId'] = Role.objects.last().id
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def previous(self,request,params={}):
        RoleListctl.count-=1
        self.form["pageno"] = RoleListctl.count 
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.form['LastId'] = Role.objects.last().id
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list ==[]:
            self.form['msg'] = "NO RECORD FOUND"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    def get_template(self):
        return "RoleList.html"

    # Service of Role
    def get_service(self):
        return RoleService()

    def deleteRecord(self, request, params={}):
        self.form['pageno'] = RoleListctl.count
        
        print("-----deleterecord page no----",self.form["pageno"])
        if (bool(self.form["ids"])== False):
            self.form["error"] = True
            self.form["message"] = "Please select atleast one checkbox"
            record = self.get_service().search(self.form)
            print("-----------delete record------",record)
            self.page_list = record["data"]
            self.form['LastId'] = Role.objects.last().id
            return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list = record["data"]

                id = int(ids)
                if (id > 0 ):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        record = self.get_service().search(self.form)
                        self.page_list = record["data"]
                        self.form["pageno"] =1
                        self.form["error"] = False
                        self.form["message"] = "Data is Sucessfully deleted"
                        print("---------->",self.page_list)
                        res= render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted "
                        res= render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res
                        










        
        

        
