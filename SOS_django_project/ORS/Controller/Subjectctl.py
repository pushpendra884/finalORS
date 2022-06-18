from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import Subject
from Service.forms import SubjectForm
from Service.service.SubjectService import SubjectService
from Service.service.CollegeService import CollegeService
from Service.service.CourseService import CourseService

class Subjectctl(BaseCtl):

    def preload (self,request):
        self.page_list = SubjectService().preload(self.form)
        self.page_list = CourseService().preload(self.form)
        self.preload_data= self.page_list

    # Populated form from Http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDescription"] = requestForm["subjectDescription"]
        self.form["course_ID"] = requestForm["course_ID"]

    # Populate Form from Model
    def model_to_form(self,obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["subjectName"] = obj.subjectName
        self.form["subjectDescription"] = obj.subjectDescription
        self.form["course_ID"] = obj.course_ID
        # self.form["courseName"] = CourseService().find_by_unique_key(self.form["course_ID"]).courseName
        self.form["courseName"]=obj.courseName
    # Convert Form into Module
    def form_to_model(self,obj):
        c= CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.subjectName = self.form["subjectName"]
        obj.subjectDescription = self.form["subjectDescription"]
        obj.course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["subjectName"])):
            inputError["subjectName"] = "subjectName can not be Null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["subjectName"])):
                inputError["subjectName"] = "subjectName should be alphabates"
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["subjectDescription"])):
            inputError["subjectDescription"] = "subjectDescription can not be Null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course Name can not be Null"
            self.form["error"] = True

        else:
            c = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form['courseName'] = c.courseName

        return self.form["error"]

        
    
        # Display MarksheetPage
    def display(self,request,params={}):
        if (params["id"]> 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
        return res

        # Submit MarksheetPage

    def submit(self,request,params={}):
        if params["id"] > 0:
            pk =params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(subjectName = self.form["subjectName"])
            if dup.count()>0:
                self.form["error"] =True
                self.form["message"] ="Subject Name is already Exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = " Data is sucessfully updated"
                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res

        else:
            duplicate = self.get_service().get_model().objects.filter(subjectName=self.form["subjectName"])
            if duplicate.count()>0:
                self.form["error"] = True
                self.form["message"] = "subjectName is already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r= self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["id"]= r.id
                self.form["error"]= False
                self.form["message"]= "Data is sucessfully saved"

                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res

     # Template html of student page
    def get_template(self):
        return "Subject.html"

    # Service of Student
    def get_service(self):
        return SubjectService()
