from django.shortcuts import render, HttpResponse
from home.models import details
from django.template import loader

from passlib.hash import bcrypt

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

# from .models import Comment
# from .forms import CommentForm

# Create your views here.

t_no=1
t_name=""
msg ={"msg":"team name already exits"}


def landing_page(request):
    return render(request,"landing_page.html")

def reffer(request):
    response = redirect('/zerohour/register/page1/')
    return response

def index(request):
    # context = {
    #     "var": "sent"
    # }
    if 't_name' in request.COOKIES:
        t_name = request.COOKIES['t_name']
        msg={'t_name':t_name}
        return render(request,"done.html",msg)

    msg ={"msg":""}
    return render(request, "home.html",msg)


def register(request):
    global t_no
    global t_name
    t_no = request.POST.get("t_no")
    t_name = request.POST.get("t_name")


    if 't_name' in request.COOKIES:
        t_name = request.COOKIES['t_name']
        mag={'t_name':t_name}
        return render(request,"done.html",mag)

    if t_name:

        if int(t_no) in [1,2,3,4]:
            global msg
            context ={"t_no":t_no,"msg":""}
                
            # if details.objects.filter(t_name=t_name).first()==None:
            #     return render(request,"better2.html",context)
            # else:
            #     return render(request,"home.html",msg)
            # check_exis(t_name)
            if details.objects.filter(t_name=t_name).first()!=None:
                return render(request,"home.html",msg)# goes to
            return render(request,"better2.html",context) #goes to submitted

        else:
            return HttpResponse("ERROR 404")
    else:
        return HttpResponse("ERROR 404")


def submitted(request):
    global t_no
    global t_name
    # print(type(t_no),t_no)
    # print(type(t_name),t_name)
    # print(request.method)
 
    if 't_name' in request.COOKIES:
        t_name = request.COOKIES['t_name']
        msg={'t_name':t_name}
        return render(request,"done.html",msg)
    if request.method == "POST":
        l_name = request.POST.get("l_name")
        l_mail = request.POST.get("l_mail")
        l_phone = request.POST.get("l_phone")
        name2 = request.POST.get("name2")
        mail2 = request.POST.get("mail2")
        name3 = request.POST.get("name3")
        mail3 = request.POST.get("mail3")
        name4 = request.POST.get("name4")
        mail4 = request.POST.get("mail4")
        password = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        
        # ->10
        # print("\n hurupa\n")
        # print(type(l_phone),l_phone)
        if 't_name' in request.COOKIES:
            request.COOKIES['t_name']
            msg={'t_name':t_name}
            return render(request,"done.html",msg)

        #confirm passwords
        if password!=pass2:
            msg ={"msg":f"Passwords don't match","t_no":t_n}
            return render(request,"better2.html",msg)


                #  Begin reCAPTCHA validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        # End reCAPTCHA validation 

        # print("\n",result['success'])
        if result['success']==False:
            msg ={"msg":f"You are a Robot","t_no":t_no}
            return render(request,"better2.html",msg)
        
        # print(type(l_phone))
        # if type(l_phone)!=int:
        #     msg ={"msg":f"Phone number must be integer"}
        #     return render(request,"better2.html",msg)




        # checking data
        if details.objects.filter(t_name=t_name).first()!=None and t_name !="":
            msg ={"msg":f"{t_name} already taken","t_no":t_no}
            return render(request,"better2.html",msg)

        if details.objects.filter(l_name=l_name).first()!=None:
            msg ={"msg":f"{l_name} already has a team","t_no":t_no}
            return render(request,"better2.html",msg)
        
        if details.objects.filter(l_phone = l_phone).first()!=None:
            msg ={"msg":f"{l_phone} is being used by another team member","t_no":t_no}
            return render(request,"better2.html",msg)

        if details.objects.filter(l_mail=l_mail).first()!=None:
            msg ={"msg":f"{l_mail} is being used by another team member","t_no":t_no}
            return render(request,"better2.html",msg)
            # 2
        if details.objects.filter(name2=name2).first()!=None and name2!="":
            print(details.objects.filter(name2=name2).first())
            msg ={"msg":f"{name2} already has a team","t_no":t_no}
            return render(request,"better2.html",msg)
        if details.objects.filter(mail2=mail2).first()!=None and mail2 !="":
            msg ={"msg":f"{mail2} is being used by another team member","t_no":t_no}
            return render(request,"better2.html",msg)
        # 3
            
        if details.objects.filter(name3=name3).first()!=None and name3!="":
            msg ={"msg":f"{name3} already has a team","t_no":t_no}
            return render(request,"better2.html",msg)
        if details.objects.filter(mail3=mail3).first()!=None and mail3 !="":
            msg ={"msg":f"{mail3} is being used by another team member","t_no":t_no}
            return render(request,"better2.html",msg) 
        # 4
        if details.objects.filter(name4=name4).first()!=None and name4!="":
            msg ={"msg":f"{name4} already has a team","t_no":t_no}
            return render(request,"better2.html",msg)
        if details.objects.filter(mail4=mail4).first()!=None and  mail4 !="":
            msg ={"msg":f"{mail4} is being used by another team member","t_no":t_no}
            return render(request,"better2.html",msg)
        
        # checking done

        hashed = bcrypt.hash(password)
        
        f = details(t_no = int(t_no),t_name=t_name, l_name=l_name, l_mail=l_mail, l_phone=int(l_phone), name2=name2,mail2=mail2, name3=name3, mail3=mail3, name4=name4, mail4=mail4, password=hashed)
        f.save()
        few={"t_name":t_name}
        response = render(request,"done.html",few)
        response.set_cookie("t_name",t_name)
        return response

    else:
        return HttpResponse("Error")




def submitted2(request):
    return render(request,"done2.html")
    


