from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from JobModel.models import User, job_item, recruiter

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return redirect(reverse("index"))

def get_user_name_and_type(request_obj):
    context = {}
    if "user" in request_obj.session and "name" in request_obj.session["user"] and "user_type" in request_obj.session["user"]:
            print("user access index page:" + request_obj.session["user"]["name"])
            context['username'] = request_obj.session["user"]["name"]
            context['user_type'] = request_obj.session["user"]["user_type"]
            
    else:
        print("guest access index page")
        context['username'] = "logout"
        context['user_type'] = "logout"
    return context

def index(request):
    context =  get_user_name_and_type(request)
    # if context["user_type"] == "recruiter":
    #     return redirect(reverse("recruiter_page"))
    print(hash(request))
    return render(request, 'index.html', context)

def my_resume(request):
    return render(request, 'dashboard.html', )

def recruiter_page(request):
    context =  get_user_name_and_type(request)
    # if context["user_type"] == "candidate":
    #     return redirect(reverse("index"))
    return render(request, 'recruiter_page.html', context)

def dashboard(request):
    context =  get_user_name_and_type(request)
    username = context["username"]
    usertype = context["user_type"]
    if usertype == "candidate":
        query_user = User.objects.filter(username=username)[0]
        user_resume_url = query_user.resume_url
        context["resume_url"] = user_resume_url
    elif usertype == "recruiter":
        query_company = recruiter.objects.filter(company_name=username)[0]
        context["company_name"] = query_company.company_name
        context["company_info"] = query_company.info
        context["company_describe"] = query_company.describe
    else:
        return redirect(reverse("login_page"))
    
    return render(request, 'dashboard.html',context )

def login_page(request):
    return render(request, 'login_page.html', )

def register_page(request):
    return render(request, 'register_page.html', )

def user_login(request):
    try:
        if request.POST:
            request.encoding='utf-8'
            if 'username' in request.POST and request.POST['username']:
                username = request.POST['username']
                if 'password' in request.POST and request.POST['password']:
                    password = request.POST['password']
                    message = ""
                else:
                    raise Exception('error: empty password')
            else:
                 raise Exception('error: empty user name')
            query_user = User.objects.filter(username=username)
            query_company = recruiter.objects.filter(company_name=username)
            if len(query_user) >= 1:
                user_type = "candidate"
                query_list = query_user
            elif len(query_company) >= 1:
                user_type = "recruiter"
                query_list = query_company
            else:
                raise Exception("error: user not existed, please register.")  
            if query_list[0].password == password:
                request.session['user'] = {}
                request.session['user']["name"] = username
                request.session['user']["user_type"] = user_type
            else:
                raise Exception("error: wrong password")  
            
            if user_type == "recruiter":
                return redirect(reverse("recruiter_page"))
            else:
                return redirect(reverse("index"))

                
        else:
            raise Exception("not support get")
    except Exception as e:
        message= str(e)
        return HttpResponse(message)

def user_logout(request):
    if "user" in request.session:
        request.session.pop("user")
    return redirect(reverse("index"))

def user_register(request):
    # if request.POST:
    try:
        massage = "pass"
        print (request.POST["people_type"])
        if request.POST["people_type"] == "candidate":
            username = request.POST["username"]
            if request.POST["password"] == request.POST["password_confirm"]:
                password = request.POST["password"]
                if len(User.objects.filter(username=username)) == 0:
                    new_user = User(username=username,password=password,resume_url="")
                    new_user.save()
                else:
                    raise ( "error : user existed, please login")
            else:
                raise ( "error : password is not same as password_confirm")
        else:
            company_name = request.POST["username"]
            company_location = request.POST["company_location"]
            company_description = request.POST["company_description"]
            if request.POST["password"] == request.POST["password_confirm"]:
                password = request.POST["password"]
                if len(recruiter.objects.filter(company_name=company_name)) == 0:
                    new_company = recruiter(company_name=company_name,password=password,info=company_location,describe=company_description,user_type="recruiter")
                    new_company.save()
                else:
                    raise ( "error : company existed, please login")
            else:
                raise ( "error : password is not same as password_confirm")
        return HttpResponse("user has been added")
    except Exception as e:
        massage = str(e)
        return HttpResponse(str(e))
        

def add_job(request):
    if request.POST:
        if "job_title" in request.POST and\
            "company" in request.POST and\
            "location" in request.POST and\
            "salary" in request.POST and\
            "requirements" in request.POST:
            print(request.POST["requirements"])
            job_title = request.POST["job_title"]
            company = request.POST["company"]
            location = request.POST["location"]
            salary = request.POST["salary"]
            requirement = request.POST["requirements"]
            new_job = job_item(job_title=job_title,company=company,location=location,salary=salary,requirement=requirement,describe="hash_"+str(hash(request)))
            new_job.save()
        else:
            raise Exception("please fiil up or args")
        return redirect(reverse("dashboard"))
