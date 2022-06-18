from pathlib import Path
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from Service.utility.DataValidator import DataValidator
from Service.service.UserService import UserService

class Loginctl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]


    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "login id can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        self.form["out"]= params.get("out")
        res = render(request,self.get_template(),{"form": self.form})
        # print("------------->",self.get_template(),self.form)
        return res

    def submit(self, request, params={}):
        PATH = params.get("path")
        user = self.get_service().authenticate(self.form)
        if (user is None):
            self.form["error"] = True
            self.form["message"] = "Invalid id or Password"
            res = render (request,self.get_template(),{"form":self.form})
            print("----Buisness Validation-->",self.get_template(),self.form)
        else :
            request.session["user"] = user
            # print("----------request.session----------",user)
            request.session["name"] = user.role_Name
            print("-------User role Name-------",user.role_Name)
            if PATH in (None , '/ORS/Home/' , '/ORS/Login/','/ORS/ForgetPassword/','/ORS/Registration/','/auth/Logout/'):
                res = redirect('/ORS/Welcome')
            # self.form ["message"] = "LOGIN SUCCESSFULLY"
            else:
                res = redirect(PATH)  
                print("-------front controller-----",res)         
        return res

    def get_template(self):
        return "Login.html"

    def get_service(self):
        return UserService()

        




