
from django.http import HttpResponse
from abc import ABC , abstractmethod
from django.shortcuts import render ,redirect

# Base class is inherited by all application controller

class BaseCtl(ABC):
    #contains preload data.
    preload_data = {}

    # Contains list of objects,it will displayed at list page
    page_list ={}

    # Initialize controller attributes
    def __init__(self):
        self.form = {}
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}
        self.form["pageno"] = 1


        # It loads preload data of the page

    def preload(self,request):
        print("This is preload data")

    '''Execute method is executed for each http request
    In it turns calls Display() or submit method for HTTP GET and
    HTTP POST methods'''

    def execute(self,request,params={}):
        print("this is executed")
        self.preload(request)
        if "GET"== request.method:
            return self.display(request,params)
        elif "POST" == request.method:
            self.request_to_form(request.POST)
            if self.input_validation():
                print("------BaseCtl inputvalidation request = {}, params = {}".format(request,params))
                return self.display(request,params)
                # return render(request,self.get_template(), {"form":self.form,})
            else :
                if (request.POST.get("operation") == "Delete"):
                    return self.deleteRecord(request,params)
                elif (request.POST.get("operation") == "next"):
                    return self.next(request,params)
                elif (request.POST.get("operation") == "previous"):
                    return self.previous(request,params)
                else:
                    print("------BaseCtl submit request = {}, params = {}".format(request,params))
                    return self.submit(request,params)
        else:
            message = "request is not supported"
            return HttpResponse (message)
    
    '''
    Delete records of Recived id
    '''
    # @abstractmethod

    def deleteRecord(self,request, params={}):
        pass

    '''
    Display records of Recived id
    '''

    @abstractmethod

    def display(self,request, params={}):
        pass


    '''
    Submit data
    '''

    @abstractmethod
    def submit(self, request, params={}):
        pass

    
    '''Populated  values from request POST/GET to controller of the object '''

    
    def request_to_form(self,requestFrom):
        pass

    '''Populate Form from Model'''

    # @abstractmethod
    def request_to_model(self,obj):
        pass

    # Convert form into modle
    def form_to_model(self, obj):
        pass

    # Apply input validations
    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""

    '''returns template to controller'''

    @abstractmethod
    def get_template(self):
        pass 

    @abstractmethod
    def get_service(self):
        pass 

    





        