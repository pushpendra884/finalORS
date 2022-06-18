from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from Service.utility.DataValidator import DataValidator
from Service.service.ForgetPasswordService import ForgetPasswordService
from Service.service.EmailService import EmailService
from Service.service.EmailMessage import EmailMessage
from Service.models import User
from ORS.utility.DataValidator import DataValidator
class ForgetPasswordctl(BaseCtl):
    def request_to_form(self, requestFrom):
        self.form["login_id"] = requestFrom["login_id"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["login_id"]):
            inputError["login_id"] = "Login can not be Null"
            self.form["error"] = True
        if DataValidator.isNotNull(self.form["login_id"]):
            if DataValidator.isemail(self.form["login_id"]):
                inputError["login_id"] = "Email id should be correct"
                self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        res = render(request,self.get_template(),{"form" : self.form})
        return res

    def submit(self, request, params={}):
        q = User.objects.filter(login_id =self.form["login_id"])
        userList = ""
        for userData in q:
            userList = userData
        if userList != "":
            emsg = EmailMessage()
            emsg.to = [userList.login_id]
            emsg.subject = "Forget Password"
            mailResponse = EmailService.send(emsg, "forgotPassword", userList)
            if mailResponse == 1:
                self.form["error"] = False
                self.form["message"] = "PLEASE CHECK YOUR MAIL ,PASSWORD IS SEND SUCESSFULLY"
                res = render(request, self.get_template(),{"form" : self.form})
                request.session["user"] = userList
                res = render(request,self.get_template(),{"form":self.form})
                
            else:
                self.form["error"] =True
                self.form["message"] = "Please Check Your Internet Connection "
                res = render(request,self.get_template(),{"form":self.form})
        else:
            self.form["error"] =True
            self.form["message"] = "Login id is not correct "
            res = render(request,self.get_template(),{"form":self.form})

        return res

         # Template html of Role page    
    def get_template(self):
        return "ForgetPassword.html"

        # Service of Role

    def get_service(self):
        return ForgetPasswordService()







