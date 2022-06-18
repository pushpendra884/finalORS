from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import TimeTable
from Service.forms import TimeTableForm
from Service.service.TimeTableService import TimeTableService
from Service.service.CollegeService import CollegeService
from Service.service.CourseService import CourseService
from Service.service.SubjectService import SubjectService

class TimeTablectl(BaseCtl):
    def preload(self,request):
        self.course_List = CourseService().preload(self.form)
        self.subject_List = SubjectService().preload(self.form)

    #Populate Form from HTTP Request

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["examTime"] = requestForm["examTime"]
        self.form["examDate"] = requestForm["examDate"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        self.form["semester"] = requestForm["semester"]

    # Populate Form from model

    def model_to_form(self, obj):
        if (obj == None):
            return None
            
        self.form["id"]=obj.id
        self.form["examTime"]=obj.examTime
        self.form["examDate"]=obj.examDate.strftime("%Y-%m-%d")
        self.form["subject_ID"]=obj.subject_ID
        self.form["course_ID"]=obj.course_ID
        self.form["semester"]=obj.semester
        self.form["courseName"]=obj.courseName
        self.form["subjectName"]=obj.subjectName

    # Convert form into module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.examTime = self.form["examTime"]
        obj.examDate = self.form["examDate"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.semester = self.form["semester"]
        obj.courseName = c.courseName
        obj.subjectName = s.subjectName
        return obj

    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["examTime"])):
            inputError["examTime"] = "exam time can not be Null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "exam Date can not be Null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "subject Name can not be Null"
            self.form["error"] = True
        else:
             o = SubjectService().find_by_unique_key(self.form["subject_ID"])
             self.form["subjectName"] = o.subjectName

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course Name can not be Null"
            self.form["error"] = True
        else:
             o = CourseService().find_by_unique_key(self.form["course_ID"])
             self.form["courseName"] = o.courseName


        if (DataValidator.isNull(self.form["semester"])):
            inputError["semester"] = "semester can not be Null"
            self.form["error"] = True

        return self.form["error"]

        # Display Marksheet page
    def display(self,request,params={}):
        if (params["id"]>0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_List,"subjectList":self.subject_List})
        return res

    # Submit TimeTable page
    def submit(self,request,params={}):
        if (params["id"] > 0):
            q = TimeTable.objects.exclude(id=params["id"]).filter(subject_ID = self.form["subject_ID"],examDate = self.form["examDate"],examTime =self.form["examTime"])
            print("===",q)
            if q.count()>0:
                self.form["error"] = True
                self.form["messsage"] = "exam time,exam date,subjectname already exists"
                res = render(request,self.get_template(),{"form":self.form})

            else:
                r = self.form_to_model(TimeTable())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] =False
                self.form["message"] = "Data is successfully updated"
                print("wwwwww",self.form["id"])
                res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_List,"subjectList":self.subject_List})
            
        else:
            r =self.form_to_model(TimeTable())
            self.get_service().save(r)
            self.form["id"] = r.id
            self.form["error"] = False
            self.form["message"] = "Data is successfully saved"
            res = render(request,self.get_template(),{"form":self.form})
        return res

      # Template html of TimeTable page    
    def get_template(self):
        return "TimeTable.html"          

    # Service of TimeTable
    def get_service(self):
        return TimeTableService()        


