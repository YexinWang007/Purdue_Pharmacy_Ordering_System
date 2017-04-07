from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect,HttpResponse,QueryDict
from .models import Client,Order,Drug,Wish_List,Shopping_Cart,Product
from .models import Profile
from django.forms import formset_factory
from .forms import ClientForm,OrderForm,DrugForm,BaseDrugFormSet,Wish_ListForm
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm
from django.contrib.auth.models import User
from django.db import models
import json

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error_message = ""
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            # If the user object is empty, no matching username and password were found
            if user is not None:
                #if user.is_active:
                    if user.profile.user_type == "Vendor":
                        auth_login(request, user)
                    # Redirect the user to their profile page
                        return redirect(reverse("client:home"))
                    else:
                        return HttpResponse("please go to: admin.p-ordering.tk")
                #else:
                #    error_message = "Your account is disabled"
            else:
                error_message = "Username or password incorrect"

                # The page is being loaded for the first time, so load a blank page
    else:
        form = LoginForm()
        error_message = ""
    return render(request, 'registration/login.html', {'form': form, 'error_message': error_message, })


@login_required
def index(request):
    user=request.user
    context = {'user':user}
    return render(request, 'homepage.html', context)

@login_required
def recent_order(request):
    count=0
    user=request.user
    saveList=[]
    orderList = Order.objects.filter(Q(client_obj=user) & (Q(status='new')|Q(status='filled')|Q(status='removed')|Q(status='ready')|Q(status='billing'))).order_by('date_time')
    for order in orderList:
        count=count+1
        drugList=Drug.objects.filter(order_obj=order).all()
        saveList.append([drugList,order])
        orderNum=count
        context = {'user': user, 'saveList': saveList, 'orderNum': orderNum}
        return render(request, 'recent_order.html', context)


@login_required
def completed_order(request):
    count=0
    user=request.user
    #user = Client.objects.order_by('-pk')[0]
    saveList=[]
    orderList = Order.objects.filter(Q(client_obj=user) & Q(status='complete')).order_by('date_time')
    for order in orderList:
        count=count+1
        drugList=Drug.objects.filter(order_obj=order).all()
        saveList.append([drugList,order])
    orderNum=count
    context = {'user': user, 'saveList': saveList, 'orderNum': orderNum}
    return render(request, 'complete_order.html', context)

def client_create(request):
    if request.method=='POST':
        form=ClientForm(request.POST)
        if form.is_valid():
            # instance=form.save(commit=False)
            # print(form.cleaned_data.get("client_name"))
            # print(form.cleaned_data.get("phone_number"))
            # print(form.cleaned_data.get("contact_email"))
            # instance.save()
            name = request.POST.get('client_name')
            phone = request.POST.get('phone_number')
            email = request.POST.get('contact_email')
            print(name)
            print(phone)
            print(email)
            client_obj=Client(client_name=name,phone_number=phone,contact_email=email)
            client_obj.save()
            #user = Client.objects.get(name)
            #user=client_obj
            #orderform=OrderForm()
            #context = {'user': user, 'orderform':orderform}
            #return order_create(request)
            messages.success(request, 'Form submission successful')
            #return HttpResponseRedirect(reverse('client:client_form'))
    else:
        form=ClientForm()

    context={"form":form}
    return render(request,"client_form.html",context)

def order_create(request):
    user=request.user
    #user = Client.objects.order_by('-pk')[0]
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            drug = request.POST.get('drug_name')
            brand = request.POST.get('drug_brand')
            quantity = request.POST.get('quantity')
            strength = request.POST.get('strength')
            doctor = request.POST.get('doctor_name')
            doctorEmail = request.POST.get('doctor_email')
            comment = request.POST.get('comment')
            order_obj = Order(drug_name=drug, drug_brand=brand, quantity=quantity, strength=strength, doctor_name=doctor, doctor_email=doctorEmail, comment=comment, client_obj=user)
            order_obj.save()
            return order_confirm(request)
    else:
        orderform = OrderForm()
    context = {'user': user, 'orderform':orderform}
    return render(request, 'make_order.html', context)

@login_required
def test_order(request):
    user=request.user
    #user = Client.objects.order_by('-pk')[0]
    DrugFormSet = formset_factory(DrugForm,formset=BaseDrugFormSet,min_num=1)
    if request.method == 'POST':
        drugformset = DrugFormSet(request.POST)
        #orderform = DrugForm(request.POST)
        if  drugformset.is_valid():#orderform.is_valid()
            for drugform in drugformset:
                df = drugform.cleaned_data
                drug_name = df.get('shopping_drug_name')
                drug_brand = df.get('shopping_drug_brand')
                strength = df.get('shopping_strength')
                quantity = df.get('shopping_quantity')
                cart_obj = Shopping_Cart(shopping_drug_name=drug_name, shopping_drug_brand=drug_brand, shopping_strength=strength, shopping_quantity=quantity, client_obj_shopping=user)
                cart_obj.save()
            drugformset=DrugFormSet()
            messages.success(request, 'Order Submitted to Shopping Cart Successful!')

    else:
        #orderform = OrderForm()
        drugformset= DrugFormSet()
    context = {'user': user,  'drugformset':drugformset}#'orderform':orderform
    return render(request, 'testorder.html', context)

def order_confirm(request):
    return render(request,'order_confirmation.html')

def order_list(request):
    user = Client.objects.order_by('-pk')[0]
    orderList= Order.objects.filter(client_obj=user).all()
    nested_list = []
    for i in range(0, len(orderList), 5):
        nested_list.append(orderList[i:i + 5])
    context = {'user': user,'nested_list': nested_list}
    return render(request, 'order_history.html', context)

@login_required
def product_search(request):
    flag=0
    user=request.user
    #user = Client.objects.order_by('-pk')[0]
    wishs = Wish_List.objects.filter(client_obj_wish=user).all()
    for drug in wishs:
        if request.GET.get(drug.wish_drug_name):
            drug.delete()
    if request.method == 'POST':
        wishform = Wish_ListForm(request.POST)
        if wishform.is_valid():
            drug_name = request.POST.get('wish_drug_name')
            drugList = Drug.objects.filter(drug_name=drug_name).all()
            if not drugList:
                flag=1
                wishList = Wish_List.objects.filter(client_obj_wish=user).all()
                messages.success(request, 'Product Not Exist')
            else:
                wishList = Wish_List.objects.filter(client_obj_wish=user).all()
                for w in wishList:
                    if w.wish_drug_name==drug_name:
                        flag=1
                        wishList = Wish_List.objects.filter(client_obj_wish=user).all()
                        messages.success(request, 'Product Already in The Wish List')
            if flag==0 :
                for drug in drugList:
                    brand = drug.brand
                    strength=drug.strength
                    ###price
                    wish_obj = Wish_List(wish_drug_name=drug.drug_name, wish_drug_brand=brand,wish_drug_strength=strength, client_obj_wish=user)
                    wish_obj.save()
                    wishList = Wish_List.objects.filter(client_obj_wish=user).all()
    else:
        wishList = Wish_List.objects.filter(client_obj_wish=user).all()
        wishform = Wish_ListForm()
    context = {'user': user, 'wishform': wishform, 'wishList':wishList}
    return render(request,'productsearch.html',context)

def dautocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term')
        drugs = Product.objects.filter(name__icontains=q)
        results = []
        for product in drugs:
            drug_json = {}
            drug_json['id'] = product.brand
            drug_json['label'] = product.name
            drug_json['value'] = product.name
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def shopping_cart(request):
    count=0
    user=request.user
    #user = Client.objects.order_by('-pk')[0]
    saveList = []
    if request.GET.get('mybtn'):
        #switch_status(request,user)
        order_object=Order(client_obj=user)
        order_object.save()
        drugs_in_cart = Shopping_Cart.objects.filter(client_obj_shopping=user).all()
        for drug in drugs_in_cart:
            drug_name=drug.shopping_drug_name
            drug_brand=drug.shopping_drug_brand
            strength=drug.shopping_strength
            quantity=drug.shopping_quantity
            drug_object=Drug(order_obj=order_object,name=drug_name,brand=drug_brand,strength=strength,quantity=quantity)
            drug_object.save()
            drug.delete()
    orderList = Shopping_Cart.objects.filter(Q(client_obj_shopping=user)).all()
    for drug in orderList:
        if request.GET.get(drug.shopping_drug_name):
            drug.delete()
    orderList = Shopping_Cart.objects.filter(Q(client_obj_shopping=user)).all()
    for drug in orderList:
        count = count + 1
        drug_name=drug.shopping_drug_name
        saveList.append([drug, drug_name])
    number_of_drug=count
    context = {'user': user, 'saveList': saveList, 'number_of_drug': number_of_drug}
    return render(request, 'shopping_cart.html', context)


#switch the status of orders from shopping cart to product ordered(new)
def switch_status(request,user):
    orders=Order.objects.filter(Q(client_obj=user) & Q(status='shopping')).all()
    for order in orders:
        order.status='new'
        order.save()

def permission_check_vendor(request):
    if request.user.profile.user_type != "Vendor":
        return False
    else:
        return True

