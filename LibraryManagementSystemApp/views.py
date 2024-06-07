from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import Customers, Books


# Create your views here.
class ViewBooks(ListView):
    model = Books
    template_name = "view-books.html"
    context_object_name = "book_records"

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context


def SearchBooks(request):
    if request.method == "POST":
        search_data = request.POST.get('searchquery')
        book_records = Books.objects.filter(
            Q(Name__icontains=search_data) | Q(Author__icontains=search_data) | Q(ISBN10__icontains=search_data) | Q(
                Description__icontains=search_data) | Q(Price__icontains=search_data))
        return render(request, "view-books.html", {'book_records': book_records})


def Signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    elif request.method == "POST":
        Name = request.POST.get("Name")
        Email = request.POST.get("Email")
        Phone = request.POST.get("Phone")
        Password = request.POST.get("Password")
        encrypted_password = make_password(Password)
        email_present = Customers.objects.filter(Email=Email)

        if email_present:
            return render(request, "signup.html", {"EmailPresent": "Flag for email already used."})
        else:
            customer_record = Customers(Name=Name, Email=Email, Phone=Phone, Password=encrypted_password)
            customer_record.save()
            book_records = Books.objects.all()
            return redirect("../signin/")
            # return render(request, "view-books.html", {'book_records':book_records})


def Signin(request):
    if request.method == "GET":
        return render(request, "signin.html")
    elif request.method == "POST":
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")

        Cust = Customers.objects.filter(Email=Email)
        if Cust:
            CustObj = Customers.objects.get(Email=Email)

            flag = check_password(Password, CustObj.Password)

            if flag:
                request.session["sessionvalue"] = CustObj.Name
                return render(request, "view-books.html", {"session": request.session["sessionvalue"]})
            else:
                return render(request, "signin.html", {"InvalidInput": "Flag for invalid input."})
        else:
            return render(request, "signin.html", {"InvalidInput": "Flag for invalid input."})
