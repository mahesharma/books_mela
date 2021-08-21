from django import forms
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from. models import Product,Cart,Customer,OrderPlaced
from .forms import CustomerRegister,UserProfile
from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


class ProductView(View):
    def get(self,request): 
        total_item=0
        Education = Product.objects.filter(category='E')
        Comics = Product.objects.filter(category='C')
        Magazines = Product.objects.filter(category='M')


        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        context = {
            'Education':Education,
            'Comics':Comics,
            'Magazines': Magazines,

            'total_item':total_item
        }
        return render(request,'app/home.html',context)



class ProductDetailView(View):
    def get(self,request,pk):
        details = Product.objects.get(pk=pk)
        already_exits = False
        total_item = 0
        if request.user.is_authenticated:
            already_exits = Cart.objects.filter(Q(product=details.id) & Q(user=request.user)).exists()
            total_item = len(Cart.objects.filter(user=request.user))

        context = {
            'details':details,
            'already_exits':already_exits,
            'total_item': total_item
        }
        return render(request,'app/productdetail.html',context)





@login_required
def add_to_cart(request):
    user = request.user
    pid = request.GET.get('prod_id')
    product = Product.objects.get(id=pid)
    Cart(user=user,product=product).save()
    return redirect('/showcart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
          
        amount = 0.0
        shipping_amt = 70.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discounted_price)
                amount+=temp_amt
                total_amt = shipping_amt+amount
            context = {
            'cart':cart,
            'amount':amount,
            'total':total_amt,
            'total_item':total_item
            }

            return render(request, 'app/addtocart.html',context)
        else:
            return render(request, 'app/message.html')




def plus_minus(request):
    if request.method=="GET":
        user=request.user
        prod_id=request.GET['prod_id']
        pk=request.GET['pk']
        
        Qid = Cart.objects.get(Q(product=prod_id) & Q(user =request.user))
        print("qid is")
        print(Qid.quantity)
        if pk == '1':
            Qid.quantity+=1
            Qid.save()
        elif pk == '2':
            Qid.quantity-=1 
            Qid.save()   
        elif pk =='3':
            Qid.delete()        
        
        amount = 0.0
        total_amt=0.0
        shipping_amt = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
                temp_amt = (p.quantity * p.product.discounted_price)
                amount+=temp_amt
                total_amt = shipping_amt+amount
       
        data = {
            'quantity':Qid.quantity,
            'amount':amount,
            'total':total_amt

            }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')



@login_required
def address(request):
    add= Customer.objects.filter(user=request.user)
    context = {
        "form":add,
        "active":"btn-primary",
    }
    return render(request, 'app/address.html',context)
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    context = {
        'order':op
    }
    return render(request, 'app/orders.html',context)

def change_password(request):
    messages.success(request, 'Account created!! Please Login')
    return render(request, 'app/changepassword.html')

def education(request,data=None):
    if data is None:
        maths = Product.objects.filter(category='E')
    elif data =='Science' or data == 'Hindi' or data == 'English' or data == 'Sst' or data == 'Maths':
        maths = Product.objects.filter(category='E').filter(brand = data)  

    context = {
        'maths': maths,
    }
    return render(request, 'app/education.html',context)

def comic(request,data=None):
    if data is None:
        comic = Product.objects.filter(category='C')
    elif data =='Marvel' or data == 'DC':
        comic = Product.objects.filter(category='C').filter(brand = data)  

    context = {
        'comic': comic,
    }
    return render(request, 'app/comics.html',context)    

def magazine(request,data=None):
    if data is None:
        magazine = Product.objects.filter(category='M')
    elif data =='Computer' or data == 'Business' or data == 'Automobile':
        magazine = Product.objects.filter(category='M').filter(brand = data)  

    context = {
        'magazine': magazine,
    }
    return render(request, 'app/magazines.html',context)    




@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amt = 70.0
    totalamount = 0.0   
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
                temp_amt = (p.quantity * p.product.discounted_price)
                amount+=temp_amt
        totalamount = amount+shipping_amt
    context ={
        'address':address,
        'totalamount':totalamount,
        'cart_items':cart_items
    }
    return render(request, 'app/checkout.html',context)

@login_required    
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,cutomer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegister()
        context = {
            'form':form,
        }
        return render(request, 'app/customerregistration.html',context)
    def post(self,request):
        form = CustomerRegister(request.POST)
        if form.is_valid():
            form.save()   
            form = CustomerRegister()  
            messages.success(request, 'Account created!! Please Login')
            return HttpResponseRedirect('/accounts/login/')
        context = {
            'form':form,
        }  
        return render(request, 'app/customerregistration.html',context)


@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form = UserProfile()
        context = {
            'form':form,
            'active':'btn-primary'
        }
        return render(request,'app/profile.html',context)
    def post(self,request):
        user = request.user
        form = UserProfile(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            states = form.cleaned_data['states']
            pincode = form.cleaned_data['pincode']
            reg = Customer(user = user,name = name,locality=locality,city=city,states=states,pincode=pincode)
            reg.save()
            form=UserProfile()
            messages.success(request, 'Details Saved!!')
        context = {
            'form':form,
            'active':'btn-primary'
        }    
        return render(request,'app/profile.html',context)
            




