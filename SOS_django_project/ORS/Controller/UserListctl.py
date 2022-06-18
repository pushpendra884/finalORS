
from django.shortcuts import render,redirect
from Service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from Service.service.UserService import UserService
from Service.models import User
from .BaseCtl import BaseCtl



class UserListctl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName",None)
        self.form["lastName"] =  requestForm.get( "lastName", None) 
        self.form["login_id"] =  requestForm.get( "login_id", None) 
        self.form["ids"]= requestForm.getlist( "ids", None)
        print("+++++++request_to_form ++++++++++",self.form)
        

    def display(self,request,params={}):
        UserListctl.count = self.form['pageno']
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        self.form['LastId'] = User.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list,"form":self.form})
        print("Display method of userlistctl-----------",self.form,request,self.page_list)
        print("--------------last id on userctl",self.form["LastId"])
        return res

    def next(self, request, params={}):    
        UserListctl.count+=1
        self.form["pageno"]=UserListctl.count
        record = self.get_service().search(self.form)
        self.form['LastId'] = User.objects.last().id
        self.page_list=record["data"]
        res = render(request, self.get_template(), {"pageList": self.page_list,"form":self.form})
        print("clicking on next button this block will run----->",self.form["pageno"])
        return res
   
    def previous(self, request, params={}):    
        UserListctl.count-=1
        self.form["pageno"]=UserListctl.count
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
       
        res = render(request, self.get_template(), {"pageList": self.page_list,"form":self.form})
        print("clicking on previous button this block will run----->",self.form["pageno"])
        return res

    def deleteRecord(self,request,params={}):
        self.form["pageno"]=UserListctl.count
        if(bool(self.form["ids"])==False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            record = self.get_service().search(self.form)
            self.page_list=record["data"]
            return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list=record["data"]                
                id=int(ids)
                print("----selecting one item----",self.form["ids"])
                if( id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form["pageno"]=1
                        record = self.get_service().search(self.form)
                        self.page_list=record["data"]
                        
                        UserListctl.count = 1

                        self.form["error"] = False
                        self.form["message"] = "DATA IS SUCCESSFULLY DELETED"
                        print("ppppppp-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res =  render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res
    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        if self.page_list ==[]:
            self.form['msg'] = "NO RECORD FOUND"
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res
        
    def get_template(self):
        return "UserList.html" 
    # Service of Role     

    def get_service(self):
        return UserService()        




    
