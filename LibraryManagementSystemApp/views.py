from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer


# Create your views here.
def Signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    elif request.method == "POST":
        Name = request.POST.get("Name")
        Email = request.POST.get("Email")
        Phone = request.POST.get("Phone")
        Password = request.POST.get("Password")
        encrypted_password = make_password(Password)

        email_present = Customer.objects.filter(Email=Email)

        if email_present:
            return render(request, "signup.html", {"EmailPresent": "Flag for email already used."})
        else:
            customer_record = Customer(Name=Name, Email=Email, Phone=Phone, Password=encrypted_password)
            customer_record.save()
            pet_records = Pet.objects.all()
            return redirect("../login-user/")
            # return render(request, "view-pets.html", {'pet_records':pet_records})


def Signin(request):
    if request.method == "GET":
        return render(request, "signin.html")
    elif request.method == "POST":
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")

        cust = Customer.objects.filter(email=Email)
        if cust:
            custobj = Customer.objects.get(email=Email)

            flag = check_password(Password, custobj.password)

            if flag:
                request.session["sessionvalue"] = custobj.name
                return render(request, "view-pets.html", {"session": request.session["sessionvalue"]})
            else:
                return render(request, "login-user.html", {"InvalidInput": "Flag for invalid input."})
        else:
            return render(request, "login-user.html", {"InvalidInput": "Flag for invalid input."})
