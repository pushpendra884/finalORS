
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class Homectl(BaseCtl):
    def display(self, request, params={}):
        print("--------------------->")
        return render(request,self.get_template())

    def submit(self,request,params={}):
        pass


# Template html of role page
    def get_template(self):
        return "home.html"

# Service of Role page
    def get_service(self):
        return "Roleservice()"


