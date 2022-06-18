
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from Service.utility.DataValidator import DataValidator
from Service.service.UserService import UserService

class Logoutctl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form["login_Id"] = requestFrom["login_Id"]
        self.form["password"] = requestFrom["password"]


    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if(DataValidator.isNull(self.form["login_Id"])):
            inputError["login_Id"] = "Login can not be null"
            self.form["error"]  = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"]  = True

        return self.form["error"]

    def display(self,request,params={}):
        request.session["user"] = None
        self.form["message"] = "Logout Sucessful"
        res = render(request,self.get_template(),{"form":self.form})
        return res

    def submit(self, request, params={}):
        pass

    # Template Html of Role page
    def get_template(self):
        return "Login.html"

    #  service of Role
    def get_service(self):
        return UserService()
        
        

    

        

        