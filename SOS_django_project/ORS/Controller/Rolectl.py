from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import College, Role
from Service.forms import RoleForm
from Service.service.RoleService import RoleService

class Rolectl(BaseCtl):
    #  Populated Form from HTTP request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]
        
    # Populate Form from model~
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    # convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.description = self.form["description"]
        return obj


    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["name"])):
            inputError["name"] = "Name can not be Null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form["name"])):
            if (DataValidator.isaplhacheck(self.form["name"])):
                inputError["name"] = "Name should be alphabatic"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["description"])):
            inputError["description"] = "Description can not be Null"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self,request,params={}):
        if (params["id"] > 0 ):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form})
        return res

    # submit Role page

    def submit(self, request, params={}):
        if params["id"] > 0:
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(name= self.form["name"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Roll name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Role())
                self.get_service().save(r)
                self.form["id"]= r.id
                self.form["error"] = False
                self.form["message"] = "Data is sucessfully Updated"
                res = render(request,self.get_template(),{"form":self.form})
            return res 
        else:
            duplicate = self.get_service().get_model().objects.filter(name=self.form["name"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Roll name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Role())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is sucessfully saved"
                res = render(request,self.get_template(),{"form":self.form})
            return res

             # Template html of Role page    
    def get_template(self):
        return "Role.html"          

    # Service of Role     
    def get_service(self):
        return RoleService()        


            









        


