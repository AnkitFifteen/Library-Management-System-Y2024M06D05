from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, Book, Cart


# Create your views here.
class ViewBooks(ListView):
    model = Book
    template_name = "view-books.html"
    context_object_name = "book_records"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            data = self.request.session['sessionvalue']
            # context = super().get_context_data(**kwargs)
            context['session'] = data
            return context
        finally:
            return context


class BookDetails(DetailView):
    model = Book
    template_name = "book-details.html"
    context_object_name = "book"


def SearchBooks(request):
    if request.method == "POST":
        search_data = request.POST.get('searchquery')
        book_records = Book.objects.filter(
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
        email_present = Customer.objects.filter(Email=Email)

        if email_present:
            return render(request, "signup.html", {"EmailPresent": "Flag for email already used."})
        else:
            customer_record = Customer(Name=Name, Email=Email, Phone=Phone, Password=encrypted_password)
            customer_record.save()
            book_records = Book.objects.all()
            return redirect("../signin/")
            # return render(request, "view-books.html", {'book_records':book_records})


def Signin(request):
    if request.method == "GET":
        return render(request, "signin.html")
    elif request.method == "POST":
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")

        Cust = Customer.objects.filter(Email=Email)
        if Cust.exists():
            CustObj = Customer.objects.get(Email=Email)

            flag = check_password(Password, CustObj.Password)

            if flag:
                request.session["sessionvalue"] = CustObj.Name
                request.session["sessionemail"] = CustObj.Email
                # book_records = Book.objects.all()
                return redirect('ViewBooks')
                # return render(request, "view-books.html", {"session": request.session["sessionvalue"],'book_records':book_records})
            else:
                return render(request, "signin.html", {"InvalidInput": "Flag for invalid input."})
        else:
            return render(request, "signin.html", {"InvalidInput": "Flag for invalid input."})


def Signout(request):
    del (request.session['sessionvalue'])
    return redirect('../signin/')


def AddToCart(request):
    if request.method == "GET" or not request.session["sessionvalue"]:
        return redirect('../signin/')
    
    if request.method == "POST" and request.session["sessionvalue"]:
        productid = request.POST.get('ProductID')
        sessionemail = request.session['sessionemail']  # email of customer
        custobj = Customer.objects.get(Email=sessionemail)  # fetch record from database table using email
        custid = custobj.id  # fetch customer id using customer object
        bobj = Book.objects.get(id=productid)

        flag = Cart.objects.filter(CID=custobj.id, PID=bobj.id)
        if flag:
            cartobj = Cart.objects.get(CID=custobj.id, PID=bobj.id)
            cartobj.Quantity = cartobj.Quantity + 1
            cartobj.Total_Amount = bobj.Price * cartobj.Quantity
            cartobj.save()
        else:
            cartobj = Cart(CID=custobj, PID=bobj, Quantity=1, Total_Amount=bobj.Price * 1)
            cartobj.save()

        return redirect('../view-books/')
    
    
def ViewCart(request):
    if request.method == "GET" and not request.session["sessionvalue"]:
        return redirect('../signin/')
    
    if request.method == "GET" and request.session["sessionvalue"]:
        sessionemail = request.session['sessionemail'] #email of customer
        custobj = Customer.objects.get(Email = sessionemail) 
        cart_products = Cart.objects.filter(CID = custobj.id)

        return render(request,'cart.html',{'cart_products':cart_products})
    
    
def ChangeQuantity(request):
    if request.method == "GET" or not request.session["sessionvalue"]:
        return redirect('../signin/')
    
    if request.method == "POST" and request.session["sessionvalue"]:
        cemail = request.session['sessionemail']
        pid = request.POST.get('PID')
        custobj = Customer.objects.get(Email = cemail)
        pobj = Book.objects.get(id = pid)
        cartobj = Cart.objects.get(CID = custobj.id, PID=pobj.id)

        if request.POST.get('changequantitybutton') == '+':
            cartobj.Quantity = cartobj.Quantity + 1
            cartobj.Total_Amount = cartobj.Quantity * pobj.Price
            cartobj.save()

        elif request.POST.get('changequantitybutton') == '-':
            if cartobj.Quantity == 1:
                cartobj.delete()
            else:
                cartobj.Quantity = cartobj.Quantity - 1
                cartobj.Total_Amount = cartobj.Quantity * pobj.Price
                print(cartobj.Total_Amount)
                cartobj.save()

        return redirect('../view-cart/')
    

def OrderCheckout(request):
    if request.method == "GET" and not request.session["sessionvalue"]:
        return redirect('../signin/')
    
    if request.method == "GET" and request.session["sessionvalue"]:
        sessionemail = request.session['sessionemail'] 
        custobj = Customer.objects.get(email = sessionemail) 
        cart_products = Cart.objects.filter(cid = custobj.id)
        total_amount = 0
        for product in cart_products:
            total_amount += product.totalamount
        return render(request,'order-checkout.html',{'cart_products':cart_products, 'total_amount':total_amount})
