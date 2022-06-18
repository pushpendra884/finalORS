from django.shortcuts import  render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .Controller.Homectl import  Homectl
from .Controller.Loginctl import Loginctl
from .Controller.Registrationctl import Registrationctl
from .Controller.Welcomectl import Welcomectl
from .Controller.Logoutctl import Logoutctl
from .Controller.Userctl import Userctl
from .Controller.ForgetPasswordctl import ForgetPasswordctl
from .Controller.MyProfilectl import MyProfilectl
from .Controller.UserListctl import UserListctl
from .Controller.Collegectl import Collegectl
from .Controller.CollegeListctl import CollegeListctl
from .Controller.Coursectl import Coursectl
from .Controller.CourseListctl import CourseListctl
from .Controller.AddFacultyctl import AddFacultyctl
from .Controller.AddFacultyListctl import AddFacultyListctl
from .Controller.Marksheetctl import Marksheetctl
from .Controller.MarksheetListctl import MarksheetListctl
from .Controller.MarksheetMeritListctl import MarksheetMeritListctl
from .Controller.Rolectl import Rolectl
from .Controller.RoleListctl import RoleListctl
from .Controller.Studentctl import Studentctl
from .Controller.StudentListctl import StudentListctl
from .Controller.Subjectctl import Subjectctl
from .Controller.SubjectListctl import SubjectListctl
from .Controller.TimeTablectl import TimeTablectl
from .Controller.TimeTableListctl import TimeTableListctl
from .Controller.ChangePasswordctl import ChangePasswordctl

# Create your views here.
def index(request):
    res = render(request,'project.html')
    return res

@csrf_exempt
def action(request,page,action=""):  
    ctlName = page + "ctl()"
    ctlobj = eval(ctlName)
    return ctlobj.execute(request,{"id":0})

# calls respective controller with id
@csrf_exempt
def actionId(request,page ="",operation="",id=0):
    path= request.META.get("PATH_INFO")
    request.session['msg'] = None
    print("-------------",path)
    if request.session.get('user') is not None and page !="":
        ctlName = page + "ctl()"
        ctlobj =  eval(ctlName)
        res = ctlobj.execute(request,{"id":id})
        print("action Id run when session is not none----->",id,ctlName,ctlobj)
    elif page == "Registration":
        ctlName = page +"ctl()"
        ctlobj = eval(ctlName)
        res = ctlobj.execute(request,{"id":id})
    elif page == "Home":
        ctlName = page + "ctl()"
        ctlobj = eval(ctlName)
        res = ctlobj.execute(request,{"id":id})
    elif page == "ForgetPassword":
        ctlName = page +"ctl()"
        ctlobj = eval(ctlName)
        res = ctlobj.execute(request,{"id":id})

    elif page =="Login":
        ctlName = "Login" + "ctl()"
        ctlobj = eval(ctlName)
        request.session['msg'] = None
        res = ctlobj.execute(request,{"id":id})    
    else:
        ctlName = "Login" + "ctl()"
        ctlobj = eval(ctlName)
        request.session['msg'] = "Your Session has been Expired,Please Login Again"
        res = ctlobj.execute(request,{"id":id,"path":path})
    return res

        

@csrf_exempt
def auth (request, page="", operation="" , id = 0):
    if page == "Logout":
        Session.objects.all().delete()
        request.session["user"]=None
        print("$$$$$$--Logout done--$$$$$$$",Session.objects.all)
        out = "Logout Sucessfull"
        ctlName = "Login" +"ctl()"
        ctlobj = eval(ctlName)
        res = ctlobj.execute(request,{"id":id, "operation" : operation,"out":out})
        

    elif page == "Forgetpassword":
        ctlName = "Forgetpassword" + "ctl()"
        ctlobj =eval(ctlName)
        res = ctlobj.execute(request,{"id":id,"operation": operation})
    return res

def index(request):
    res = render(request,'project.html')
    return res

# TO remove favicon error
def GET(self):
    return HttpResponse("Hello Guys")

