from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render 
from ORS.utility.DataValidator import DataValidator
from Service.models import Marksheet
from Service.forms import MarksheetForm
from Service.service.StudentService import StudentService
from Service.service.MarksheetMeritListService import MarksheetMeritListService

class MarksheetMeritListctl(BaseCtl):
    count = 1
    # Display Marksheet page

    def request_to_form(self, requestForm):
        self.form['rollNumber'] = requestForm.get('rollNumber', None)
        self.form['name'] = requestForm.get('name', None)
        self.form['physics'] = requestForm.get('physics', None)
        self.form['chemistry'] = requestForm.get('chemistry', None)
        self.form['maths'] = requestForm.get('maths', None)
        self.form['ids'] = requestForm.getlist('ids', None)
   

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        print("##########",record)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res 

    # Submit MarksheetPage

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list == []:
            self.form["msg"] = "record is not found"
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res 

    # Templatehtml of Role page
    def get_template(self):
        return "MarksheetMeritList.html"

    #  Service of Role
    def get_service(self):
        return MarksheetMeritListService()
      


