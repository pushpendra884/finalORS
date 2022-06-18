from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import User
from Service.service.ChangePasswordService import ChangePasswordService
from Service.service.EmailMessage import EmailMessage
from Service.service.EmailService import EmailService 
from Service.service.UserService import UserService 

class ChangePasswordctl(BaseCtl):    
    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["newPassword"] = requestForm["newPassword"]
        self.form["oldPassword"] = requestForm["oldPassword"]
        self.form["confirmPassword"] = requestForm["confirmPassword"]

       #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id
        self.form["newPassword"] = obj.newPassword
        self.form["oldPassword"] = obj.oldPassword
        self.form["confirmPassword"] = obj.confirmPassword

        #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.newPassword=self.form["newPassword"]
        obj.oldPassword=self.form["oldPassword"] 
        obj.confirmPassword=self.form["confirmPassword"]
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["newPassword"])):
            inputError["newPassword"] = "New Password can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["oldPassword"])):
            inputError["oldPassword"] = "Old Password can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["confirmPassword"])):
            inputError["confirmPassword"] = "Confirm Password can not be null"
            self.form["error"] = True
        return self.form["error"]   

     #Display Change Password page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit Change Password page
    def submit(self,request,params={}):
        user = request.session.get("user",None)
        print("------------------>>>>>>>",user)
        q=User.objects.filter(login_id = user.login_id,password=self.form["oldPassword"])
        print("------------------------q={}".format(q))
        if q.count()>0:
            if self.form["confirmPassword"]==self.form["newPassword"]:
                convertUser=self.convert(user,user.id,self.form["newPassword"])
                UserService().save(convertUser)
                print("----------------",user.login_id,user.password)
                emgs=EmailMessage()
                emgs.to=[user.login_id]
                emgs.subject="Change Password"
                mailResponse=EmailService.send(emgs,"changePassword",user)
                print("-------------------->>>>",mailResponse)
                if(mailResponse==1):
                    
                    self.form["error"] = False
                    self.form["message"] = "YOUR PASSWORD IS CHANGED SUCCESSFULLY, PLS CHECK YOUR MAIL"
                    res = render(request,self.get_template(),{"form":self.form})
                else:
                    self.form["error"] = True
                    self.form["message"] = "Please check your net "
                    res = render(request,self.get_template(),{"form":self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Confirm password are not match"
                res = render(request,self.get_template(),{"form":self.form})
        else:
            self.form["error"] = True
            self.form["message"] = "oldPassword is wrong"
            res = render(request,self.get_template(),{"form":self.form})
        return res
     
     
    def convert(self,u,uid,upass):
        u.id=uid
        u.password=upass
        return u
    # Template html of Change Password page    
    def get_template(self):
        return "ChangePassword.html"          

    # Service of Role     
    def get_service(self):
        return ChangePasswordService()        






