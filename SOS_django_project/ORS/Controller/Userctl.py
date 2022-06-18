from django.shortcuts import render, redirect
from Service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from Service.models import User
from Service.service.UserService import UserService
from Service.service.RoleService import RoleService
from ORS.utility.DataValidator import DataValidator
class Userctl(BaseCtl):
    def preload(self, request):
        self.page_list = RoleService().preload(self.form)
        self.preloadData = self.page_list
        print("preload data give---------",self.page_list)

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = requestForm["role_Id"]
        print("#############",requestForm)

    # Populate Form from Model
    #GET-display method is call this function
    def model_to_form(self, obj):

        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address  
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = obj.role_Id
        self.form["role_Name"] = obj.role_Name
        print("!!!!!!!!!!!!!!!",obj)
    # Convert form into module
    def form_to_model(self, obj):
        c = RoleService().get(self.form["role_Id"])
        print("***********",c)
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        obj.role_Name = c.name
        print("^^^^^^^^^^^^^^^^^",obj)
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form["firstName"])):
            if (DataValidator.isaplhacheck(self.form["firstName"])):
                inputError["firstName"] = " First Name should contain alphabets"
                self.form["error"] = True
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form["lastName"])):
            if (DataValidator.isaplhacheck(self.form["lastName"])):
                inputError["lastName"] = " Last Name should contain alphabets"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNotNull(self.form["login_id"])):
            if (DataValidator.isemail(self.form["login_id"])):
                inputError["login_id"] = "Email should be in @gmail.com form"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "confirmpassword can not be null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form["confirmpassword"])):
            if (self.form["password"] != self.form["confirmpassword"]):
                inputError["confirmpassword"] = "Password and confirm Password are not Same"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "address can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "mobileNumber can not be null"
            self.form["error"] = True
        if (DataValidator.isNotNull(self.form["mobilenumber"])):
            if (DataValidator.ismobilecheck(self.form["mobilenumber"])):
                inputError["mobilenumber"] = "mobileNumber should start with 6,7,8,9"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Please select one option"
            self.form["error"] =True

        if (DataValidator.isNull(self.form["role_Id"])):
            inputError["role_Id"] = "Please select one option"
            self.form["error"] =True
        else:
            o = RoleService().find_by_unique_key(self.form["role_Id"])
            self.form["role_Name"] = o.name
         
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "roleList": self.preloadData})
        print("=====Display method shows====",self.form,self.preloadData,self.get_template())
        return res

    # Submit Role page
    def submit(self, request, params={}):
        if params["id"] > 0:
            print("===Old ID ========",params)
            pk =params["id"]
            print("ppppppppkkkkkk",pk)
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(login_id = self.form["login_id"])
            print("---------",dup)
            if dup.count()>0:
                self.form["error"] =True
                self.form["message"] ="Login Id is already Exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = " Data is sucessfully updated"
                print("===New ID ========",params,pk,dup,r)
                res = render(request,self.get_template(),{"form":self.form,"roleList": self.preloadData})
            return res

        else:
            duplicate = self.get_service().get_model().objects.filter(login_id=self.form["login_id"])
            if duplicate.count()>0:
                self.form["error"] = True
                self.form["message"] = "User is already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r= self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"]= r.id
                self.form["error"]= False
                self.form["message"]= "Data is sucessfully saved"

                res = render(request,self.get_template(),{"form":self.form,"roleList": self.preloadData})
            return res



    def get_template(self):
        return "User.html"

    # Service of Role
    def get_service(self):
        return UserService()
