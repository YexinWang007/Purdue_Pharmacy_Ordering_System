from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
# Create your views here.
from .models import Client,Order,Drug
from django.forms import formset_factory
from .forms import ClientForm,OrderForm,DrugForm,BaseDrugFormSet
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone


def index(request):
    count=0
    user = Client.objects.order_by('-pk')[0]
    saveList=[]
    orderList = Order.objects.filter(client_obj=user).all()
    for order in orderList:
        count=count+1
        drugList=Drug.objects.filter(order_obj=order).all()
        saveList.append([drugList,order])
    orderNum=count
    context = {'user': user, 'saveList': saveList, 'orderNum': orderNum}
    return render(request, 'testhome.html', context)

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
    user = Client.objects.order_by('-pk')[0]
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

def test_order(request):
    user = Client.objects.order_by('-pk')[0]
    DrugFormSet = formset_factory(DrugForm,formset=BaseDrugFormSet,min_num=1)
    if request.method == 'POST':
        drugformset = DrugFormSet(request.POST)
        #orderform = DrugForm(request.POST)
        if  drugformset.is_valid():#orderform.is_valid()
            order_obj = Order(client_obj=user)
            order_obj.save()
            for drugform in drugformset:
                df = drugform.cleaned_data
                drug_name = df.get('drug_name')
                drug_brand = df.get('drug_brand')
                strength = df.get('strength')
                quantity = df.get('quantity')
                drug_obj = Drug(drug_name=drug_name, drug_brand=drug_brand, strength=strength, quantity=quantity, order_obj=order_obj)
                drug_obj.save()
            drugformset=DrugFormSet()
            messages.success(request, 'Order Submission Successful!')

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