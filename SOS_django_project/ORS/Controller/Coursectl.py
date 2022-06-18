

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import College, Course
from Service.forms import CourseForm
from Service.service.CourseService import CourseService

class Coursectl(BaseCtl):
    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["courseName"] = requestForm["courseName"]
        self.form["courseDescription"] = requestForm["courseDescription"]
        self.form["courseDuration"] = requestForm["courseDuration"]


    def next(self,request,params={}):
        pass

    # Populate Form from Model

    def model_to_form(self,obj):
        if (obj == None):
            return

        self.form["id"] = obj.id
        self.form["courseName"] = obj.courseName
        self.form["courseDescription"] = obj.courseDescription
        self.form["courseDuration"] = obj.courseDuration

    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.courseName = self.form["courseName"]
        obj.courseDescription = self.form["courseDescription"]
        obj.courseDuration = self.form["courseDuration"]
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError =self.form["inputError"]
        if (DataValidator.isNull(self.form["courseName"])):
            inputError["courseName"] = "Name can not be Null"
            self.form["error"] = True

        else:
            if (DataValidator.isaplhacheck(self.form["courseName"])):
                inputError["courseName"] = "Course Name should be alphabate"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["courseDescription"])):
            inputError["courseDescription"] = "Description can not be Null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["courseDuration"])):
            inputError["courseDuration"] = "Duration can not be Null"
            self.form["error"] = True

        return self.form["error"]

    #Display Course Page

    def display(self,request,params={}):
        if params["id"] > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)

        res = render(request,self.get_template(),{"form":self.form})
        return res

    # Submit Role page

    def submit(self, request, params={}):
        if params["id"]>0:
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(courseName=self.form["courseName"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "CourseName already exist"
                res = render( request,self.get_template(),{"form": self.form})

            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is Sucessfully updated"
                res = render(request,self.get_template(),{"form":self.form})
            return res

        else:
            duplicate = self.get_service().get_model().objects.filter(courseName=self.form["courseName"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] ="CourseName already exist"
                res = render(request,self.get_template(),{"form":self.form})

            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is sucessfully saved"
                res = render(request,self.get_template(),{"form":self.form})
            return res
    # Template html of role page

    def get_template(self):
        return "Course.html"


     # Service of Role     
    def get_service(self):
        return CourseService()        





            




        

            
            




        



        