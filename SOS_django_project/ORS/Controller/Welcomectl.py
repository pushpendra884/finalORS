from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class Welcomectl(BaseCtl):

    def display(self,request,params={}):
        user = request.session.get("user",None)
        request.session["message"] = "Welcome"+ user.role_Name
        if(user is not None): 
            request.session['name'] = user.role_Name
            self.form["message"] = "Welcome " + user.role_Name
        return render(request,self.get_template(),{"form":self.form})

    def submit(self, request, params={}):
        return render(request,self.get_template(),{"form":self.form})

    # Template html of Role page
    def get_template(self):
        return "Welcome.html"

    # Service of Role
    def get_service(self):
        return "RoleService()"
        



