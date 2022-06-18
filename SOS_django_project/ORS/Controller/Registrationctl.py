from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from Service.utility.DataValidator import DataValidator
from Service.models import User
from Service.service.UserService import UserService 
from Service.service.RoleService import RoleService
from Service.service.EmailService import EmailService
from Service.service.EmailMessage import EmailMessage
from ORS.utility.DataValidator import DataValidator

class Registrationctl(BaseCtl):
    def preload(self,request):
        self.page_list =RoleService().search(self.form)
        self.preloadData = self.page_list

    # Populated Form  from HTTP Request
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
        self.form["roll_Id"] = 2        
        self.form["roll_Name"] = "Student"

    # populated Form from Model 
    def model_to_form(self,obj):
        if obj is None:
            return
        self.form["id"] =obj.id
        self.form["firstName"] = obj.firstname
        self.form["lastName"] = obj.lastname
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob
        self.form["address"] =obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] =obj.mobilenumber
        self.form["roll_Id"] = 2
        self.form["roll_Name"] = "student"

    # convert form into Module
    def form_to_model(self,obj):
        pk =int(self.form["id"])

        if pk > 0:
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
        obj.role_Id = self.form["roll_Id"]
        obj.roll_Name = self.form["roll_Name"]
        return obj

  # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["firstName"]):
            inputError["firstName"] = "Name can not be null" 
            self.form["error"] = True
        if DataValidator.isNotNull(self.form["firstName"]):
            if DataValidator.isaplhacheck(self.form["firstName"]):
                inputError["firstName"] = "First Name should contain alphabets" 
                self.form["error"] = True
        if DataValidator.isNull(self.form["lastName"]):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if DataValidator.isNotNull(self.form["lastName"]):
            if DataValidator.isaplhacheck(self.form["lastName"]):
                inputError["lastName"] = "last Name should contain alphabets" 
                self.form["error"] = True
        if DataValidator.isNull(self.form["login_id"]):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if DataValidator.isNotNull(self.form["login_id"]):
            if DataValidator.isemail(self.form["login_id"]):
                inputError["login_id"] = "Email should be in @gmail.com form" 
                self.form["error"] = True
        

        if DataValidator.isNull(self.form["password"]):
            inputError["password"] = "password can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form["confirmpassword"]):
            inputError["confirmpassword"] = "confirmpassword can not be null"
            self.form["error"] = True
        if DataValidator.isNotNull(self.form["confirmpassword"]):
            if self.form["password"] != self.form["confirmpassword"]:
                inputError["conpassword"] = "password and confirm password are not same"

        if DataValidator.isNull(self.form["address"]):
            inputError["address"] = "address can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form["mobilenumber"]):
            inputError["mobilenumber"] = "mobilenumber can not be null"
            self.form["error"] = True 
        if DataValidator.isNotNull(self.form["mobilenumber"]):
            if DataValidator.ismobilecheck(self.form["mobilenumber"]):
                inputError["mobilenumber"] = "mobileNumber should start with 6,7,8,9" 
                self.form["error"] = True
        if DataValidator.isNull(self.form["dob"]):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form["gender"]):
            inputError["gender"] = "Please select one option"
            self.form["error"] = True
           
        return self.form["error"]

        # Display Role page

    def display(self, request,params={}):
        if params["id"] > 0:
            r = self.get_service.get(params["id"])
            self.model_to_form(r)
        res =render(request,self.get_template(),{"form": self.form})
        return res

    # Submit Role page
    def submit(self,request,params={}):
        q = User.objects.filter()

        q= q.filter(login_id=self.form["login_id"])
        if q.count() > 0:
                self.form["error"] =True
                self.form["message"] = "Already exists"
                res = render(request,self.get_template(),{"form": self.form})
        else:
            emsg = EmailMessage()
            emsg.to = [self.form["login_id"]]
            e = {}
            e["login"] = self.form["login_id"]
            e["password"] = self.form["password"]
            emsg.subject ="ORS Registration Succsessful"
            mailResponse =EmailService.send(emsg,"signUp",e)
            if mailResponse == 1:
                r = self. form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id 
                self.form["error"] = False
                self.form["message"] = "YOU HAVE REGISTERED SUCSESSFULLY"
                res = render(request,self.get_template(),{"form": self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Please Check your internet connection"
                res = render(request,self.get_template(),{"form": self.form})
        return res

    def get_template(self):
        return "Registration.html"

        # Service of Role

    def get_service(self):
        return UserService()
        






