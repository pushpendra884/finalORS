from multiprocessing.reduction import duplicate
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from Service.models import Marksheet
from Service.forms import MarksheetForm
from Service.service.MarksheetService import MarksheetService

class Marksheetctl(BaseCtl):

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]

    # Populate Form from model
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["rollNumber"] = obj.rollNumber
        self.form["name"] = obj.name
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths

    # convert form into module
    def form_to_model(self,obj):


        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.rollNumber = self.form["rollNumber"]
        obj.name = self.form["name"] 
        obj.physics =self.form["physics"] 
        obj.chemistry = self.form["chemistry"] 
        obj.maths = self.form["maths"] 

        return obj

        # Validate form

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["rollNumber"])):
            inputError["rollNumber"] = "roll Number can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ischeckroll(self.form["rollNumber"])):
                inputError["rollNumber"] = "Roll Number should be alpha numeric and Capital"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["name"])):
            inputError["name"] = "name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["name"])):
                inputError["name"] = "please enter alphabates"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["physics"])):
            inputError["physics"] = "physics can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["physics"])):
                inputError["physics"] = "please enter number below 100"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["chemistry"])):
            inputError["chemistry"] = "chemistry can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["chemistry"])):
                inputError["chemistry"] = "please enter number below 100"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["maths"])):
            inputError["maths"] = "maths can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["maths"])):
                inputError["maths"] = "please enter number below 100"
                self.form["error"] = True

        return self.form["error"]

    # Display MarksheetPage

    def display(self,request,params={}):
        if ( params["id"] > 0):
            r =self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form})
        return res

    # Submit Marksheet page
    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(rollNumber=self.form["rollNumber"])
            if dup.count() > 0:
                self.form["error"] = True 
                self.form['message'] = "Roll number is already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully Updated"
                res = render(request, self.get_template(), {"form": self.form})
            return res

        else:
            duplicate = self.get_service().get_model().objects.filter(rollNumber = self.form["rollNumber"])
            if duplicate.count() > 0:
                self.form["error"]  = True
                self.form["message"] = "Rollnumber is already exists"
                res = render(request, self.get_template(),{"form": self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully saved"
                res = render(request, self.get_template(), {"form": self.form})
            return res 

     # Template html of Role page    

    def get_template(self):
        return "Marksheet.html"          

    # Service of Role     
    def get_service(self):
        return MarksheetService()        
     
            

                










            





        

        
