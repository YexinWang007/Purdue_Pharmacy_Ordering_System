from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect,HttpResponse,QueryDict
# Create your views here.
from .models import Client,Order,Drug,Wish_List
from django.forms import formset_factory
from .forms import ClientForm,OrderForm,DrugForm,BaseDrugFormSet,Wish_ListForm
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import json

def index(request):
    user=Client.objects.order_by('-pk')[0]
    context = {'user':user}
    return render(request, 'homepage.html', context)


def recent_order(request):
    count=0
    user = Client.objects.order_by('-pk')[0]
    saveList=[]
    orderList = Order.objects.filter(Q(client_obj=user) & (Q(status='new')|Q(status='filled')|Q(status='removed')|Q(status='ready')|Q(status='billing'))).order_by('date_time')
    for order in orderList:
        count=count+1
        drugList=Drug.objects.filter(order_obj=order).all()
        saveList.append([drugList,order])
    orderNum=count
    context = {'user': user, 'saveList': saveList, 'orderNum': orderNum}
    return render(request, 'recent_order.html', context)

def completed_order(request):
    count=0
    user = Client.objects.order_by('-pk')[0]
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

def product_search(request):
    user = Client.objects.order_by('-pk')[0]
    if request.method == 'POST':
        wishform = Wish_ListForm(request.POST)
        if wishform.is_valid():
            drug_name = request.POST.get('wish_drug_name')
            drugList = Drug.objects.filter(drug_name=drug_name).all()
            if not drugList:
                wishList = Wish_List.objects.filter(client_obj_wish=user).all()
                messages.success(request, 'Product Not Exist')
            elif drugList[0].drug_name in Wish_List:
                wishList = Wish_List.objects.filter(client_obj_wish=user).all()
                messages.success(request, 'Product Already in The Wish List')
            else :
                for drug in drugList:
                    brand = drug.drug_brand
                    strength=drug.strength
                    ###price
                    wish_obj = Wish_List(wish_drug_name=drug, wish_drug_brand=brand,wish_drug_strength=strength, client_obj_wish=user)
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
        drugs = Drug.objects.filter(drug_name__icontains=q)
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.drug_brand
            drug_json['label'] = drug.drug_name
            drug_json['value'] = drug.drug_name
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def shopping_cart(request):
    user=1
    context={'user':user}
    return render(request, 'shopping_cart.html', context)

def wish_revise(request):
    # if request.method == 'PUT':
    #     put = QueryDict(request.body)
    #     drug_pk = put['pk']
    #     drug = get_object_or_404(Drug, pk=drug_pk)
    #     if put['name'] == 'wish_drug_brand':
    #         drug.brand = put['value']
    #     elif put['name'] == 'wish_drug_name':
    #         drug.name = put['value']
    #     elif put['name'] == 'wish_drug_strength':
    #         drug.strength = put['value']
    #
    #     drug.save()
    #
    #     result = {'success': 'true', 'msg': 'failed'}
    #     oput = json.dumps(result)
    #     return HttpResponse(oput, content_type='application/json')

    if request.method == 'DELETE':
        delete = QueryDict(request.body)
        drug_pk = delete['pk']
        drug = get_object_or_404(Wish_List, pk=drug_pk)
        drug.delete()
        return HttpResponse(status=200)