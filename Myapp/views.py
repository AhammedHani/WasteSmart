import string

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from Myapp.models import *


def login(request):
    return render(request,'login_index.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    var=Login.objects.filter(username=username,password=password)
    if var.exists():

        var2=Login.objects.get(username=username,password=password)
        request.session['lid']=var2.id

        if var2.type=='admin':
            return HttpResponse('''<script>alert('ADMIN LOGIN SUCCESS');window.location='/Myapp/admin_home'</script>''')
        elif var2.type=='user':
            return HttpResponse('''<script>alert('USER LOGIN SUCCESS');window.location='/Myapp/user_home'</script>''')
        elif var2.type=='pickup':
            return HttpResponse('''<script>alert('PICKUP LOGIN SUCCESS');window.location='/Myapp/pickup_home/'</script>''')
        else:
            return HttpResponse('''<script>alert('LOGIN FAILED');window.location='/Myapp/login'</script>''')


    else:
        return HttpResponse('''<script>alert('LOGIN FAILED');window.location='/Myapp/login'</script>''')


#admin

def admin_home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request, 'admin/homepage.html')

def admin_change_password(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'admin/Change password.html')

def admin_change_password_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    currentpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    var=Login.objects.filter(id=request.session['lid'],password=currentpassword)
    if var.exists():
        print("yes")
        if newpassword==confirmpassword:
            var2 = Login.objects.filter(id=request.session['lid']).update(password=confirmpassword)
            return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location='/Myapp/login'</script>''')
        else:
            return HttpResponse('''<script>alert('PASSWORD NOT CHANGED');window.location='/Myapp/login'</script>''')
    else:
        return HttpResponse('''<script>alert('CURRENT PASSWORD IS WRONG');window.location='/Myapp/login'</script>''')


def add_category(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'admin/Add category.html')

def add_category_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    categoryname=request.POST['textfield']
    coins=request.POST['textfield2']
    var=Category()
    var.name=categoryname
    var.coins=coins
    var.save()
    return HttpResponse('''<script>alert('CATEGORY ADDED SUCCESSFULLY');window.location='/Myapp/add_category'</script>''')


def edit_category(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Category.objects.get(id=id)
    return render(request,'admin/Edit category.html',{'data':var})

def edit_category_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    categoryname=request.POST['textfield']
    coins=request.POST['textfield2']
    id=request.POST['id']
    var = Category.objects.get(id=id)
    var.name = categoryname
    var.coins=coins
    var.save()
    return HttpResponse('''<script>alert('CATEGORY UPADTED SUCCESSFULLY');window.location='/Myapp/view_category'</script>''')

def delete_category(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Category.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('CATEGORY DELETED SUCCESSFULLY');window.location='/Myapp/view_category'</script>''')

def view_category(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Category.objects.all()
    return render(request,'admin/View category.html',{'data':var})

def view_category_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    search=request.POST['textfield']
    var=Category.objects.filter(name__icontains=search)
    return render(request,'admin/View category.html',{'data':var})

def schedule(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'admin/Schedule.html')

def schedule_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    id=request.POST['id']
  #  rid=Request_sub.objects.get(id=id).REQUEST_id
    date=request.POST['textfield']
    time=request.POST['textfield2']
    pickupdriver=request.POST['driverid']
    var=Schedule()
    var.date=date
    var.time=time
    var.PICKUPDRIVER_id=pickupdriver
    # rid=Request.objects.filter(id=id).update(status='scheduled')
    var.REQUEST_SUB_id=id
    var.save()
    Request_sub.objects.filter(id=id).update(status='scheduled')
    return HttpResponse('''<script>alert('SCHEDULE SUCCESS');window.location='/Myapp/request_from_user/'</script>''')

def view_confirm_request(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Request_sub.objects.filter(status='scheduled')
    return render(request,'admin/View confirm request.html',{'data':var})

def view_confirm_request_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var = Request_sub.objects.filter(REQUEST__date__range=[fromdate, todate],status='scheduled')
    return render(request,'admin/View confirm request.html',{'data':var})

def reject_request(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Request_sub.objects.filter(status='reject')
    return render(request,'admin/View reject request.html',{'data':var})

def reject_request_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield2']
    todate=request.POST['textfield']
    var=Request_sub.objects.filter(REQUEST__date__range=[fromdate,todate],status='reject')
    return render(request,'admin/View reject request.html',{'data':var})

def view_feedback(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Feedback.objects.all()
    return render(request,'admin/View feedback.html',{'data':var})

def view_feedback_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var = Feedback.objects.filter(date__range=[fromdate, todate])
    return render(request, 'admin/View feedback.html', {'data': var})

def request_from_user(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Request_sub.objects.filter(status='pending')
    return render(request,'admin/View request from user and confirm or reject.html',{'data':var})

def request_from_user_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var=Request_sub.objects.filter(REQUEST__date__range=[fromdate,todate],status='pending')
    return render(request,'admin/View request from user and confirm or reject.html',{'data':var})

def confirm_request(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    import datetime
    dt = datetime.date.today()
    var = Request_sub.objects.get(id=id)
    var2 = Pickupdriver.objects.all()
    return render(request,'admin/Schedule.html',{'data':var, 'id':id ,'data2':var2,'dt':str(dt)})

def reject2_request(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Request_sub.objects.filter(id=id).update(status='reject')
    # id2=var.REQUEST
    # var2= Request.objects.filter(id=id2).update(status='reject')
    return HttpResponse('''<script>alert('REJECT SUCCESS');window.location='/Myapp/request_from_user/'</script>''')

def view_schedule(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Schedule.objects.all()
    return render(request,'admin/View schedule.html',{'data':var})

def view_schedule_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield2']
    todate=request.POST['textfield']
    var=Schedule.objects.filter(date__range=[fromdate,todate])
    return render(request,'admin/View schedule.html',{'data':var})

def view_users(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=User.objects.all()
    return render(request,'admin/View users.html',{'data':var})

def view_users_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    search=request.POST['textfield']
    var = User.objects.filter(name__icontains=search)
    return render(request, 'admin/View users.html', {'data': var})

def add_pickup(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'admin/Add pickup.html')

def add_pickup_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    pickupname=request.POST['textfield']
    lisenceno = request.POST['textfield2']
    place = request.POST['textfield3']
    phone = request.POST['textfield4']
    email = request.POST['textfield5']

    lobj = Login()
    lobj.username = email
    lobj.password=phone
    lobj.type='pickup'
    lobj.save()

    var=Pickupdriver()
    var.name=pickupname
    var.lisenceno=lisenceno
    var.place=place
    var.phone=phone
    var.email=email
    var.LOGIN=lobj
    var.save()
    return HttpResponse('''<script>alert('PICKUP ADDED SUCCESSFULLY');window.location='/Myapp/add_pickup'</script>''')

def view_pickup(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Pickupdriver.objects.all()
    return render(request, 'admin/View pickup.html', {'data': var})

def view_pickup_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    search=request.POST['textfield']
    var=Pickupdriver.objects.filter(name__icontains=search)
    return render(request,'admin/View pickup.html',{'data':var})

def delete_pickup(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Pickupdriver.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('PICKUP DELETED SUCCESSFULLY');window.location='/Myapp/view_pickup'</script>''')

def edit_pickup(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Pickupdriver.objects.get(id=id)
    return render(request,'admin/Edit pickup.html',{'data':var})

def edit_pickup_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    pickupname = request.POST['textfield']
    lisenceno = request.POST['textfield2']
    place = request.POST['textfield3']
    phone = request.POST['textfield4']
    email = request.POST['textfield5']
    id=request.POST['id']
    res=Pickupdriver.objects.get(id=id).LOGIN.id

    obj=Login.objects.filter(id=res).update(password=phone)

    var = Pickupdriver.objects.get(id=id)
    var.name = pickupname
    var.lisenceno = lisenceno
    var.place = place
    var.phone = phone
    var.email = email
    var.save()
    return HttpResponse('''<script>alert('PICKUP UPADTED SUCCESSFULLY');window.location='/Myapp/view_pickup'</script>''')

# pickup

def pickup_home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,"Pickup/homepage.html")

def view_pickup_profile(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Pickupdriver.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "Pickup/view profile pickup.html",{'data':var})


def view_schedule_pickup(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Schedule.objects.filter(PICKUPDRIVER__LOGIN_id=request.session['lid'])
    data = []
    for i in var:
        if Pickup.objects.filter(SCHEDULE=i).exists():
            data.append({"id": i.id, "rdate": i.REQUEST_SUB.REQUEST.date, "name": i.REQUEST_SUB.REQUEST.USER.name, "housename": i.REQUEST_SUB.REQUEST.USER.housename, "place": i.REQUEST_SUB.REQUEST.USER.place, "pin": i.REQUEST_SUB.REQUEST.USER.pin, "district": i.REQUEST_SUB.REQUEST.USER.district, "phone": i.REQUEST_SUB.REQUEST.USER.phone, "category": i.REQUEST_SUB.CATEGORY.name,  "date": i.date,
                         "status": "Picked Up"})

        else:
            data.append({"id": i.id, "rdate": i.REQUEST_SUB.REQUEST.date, "name": i.REQUEST_SUB.REQUEST.USER.name, "housename": i.REQUEST_SUB.REQUEST.USER.housename, "place": i.REQUEST_SUB.REQUEST.USER.place, "pin": i.REQUEST_SUB.REQUEST.USER.pin, "district": i.REQUEST_SUB.REQUEST.USER.district, "phone": i.REQUEST_SUB.REQUEST.USER.phone, "category": i.REQUEST_SUB.CATEGORY.name, "date": i.date,
                         "status": "Not"})

    return render(request, 'Pickup/view schedule pickup.html', {'data': data})

def view_schedule_pickup_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate = request.POST['textfield2']
    todate = request.POST['textfield']
    var = Schedule.objects.filter(PICKUPDRIVER__LOGIN_id=request.session['lid'],date__range=[fromdate,todate])
    data = []
    for i in var:
        if Pickup.objects.filter(SCHEDULE=i).exists():
            data.append({"id": i.id, "rdate": i.REQUEST_SUB.REQUEST.date, "name": i.REQUEST_SUB.REQUEST.USER.name, "housename": i.REQUEST_SUB.REQUEST.USER.housename, "place": i.REQUEST_SUB.REQUEST.USER.place, "pin": i.REQUEST_SUB.REQUEST.USER.pin, "district": i.REQUEST_SUB.REQUEST.USER.district, "phone": i.REQUEST_SUB.REQUEST.USER.phone, "category": i.REQUEST_SUB.CATEGORY.name, "date": i.date,
                         "status": "Picked Up"})

        else:
            data.append({"id": i.id, "rdate": i.REQUEST_SUB.REQUEST.date, "name": i.REQUEST_SUB.REQUEST.USER.name, "housename": i.REQUEST_SUB.REQUEST.USER.housename, "place": i.REQUEST_SUB.REQUEST.USER.place, "pin": i.REQUEST_SUB.REQUEST.USER.pin, "district": i.REQUEST_SUB.REQUEST.USER.district, "phone": i.REQUEST_SUB.REQUEST.USER.phone, "category": i.REQUEST_SUB.CATEGORY.name, "date": i.date,
                         "status": "Not"})

    return render(request, 'Pickup/view schedule pickup.html', {'data': data})


def add_quantity(request,id):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request, 'Pickup/Add quantiy pickup.html', {'id': id})


def confirm_pickup(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    id=request.POST['id']
    quantity=request.POST['textfield']
    var = Pickup()
    from datetime import  datetime
    var.date=datetime.now().strftime('%Y-%m-%d')
    var.time=datetime.now().strftime('%H:%M:%S')
    var.SCHEDULE_id=id
    var.Quantity=quantity

    var3=Coin()
    cns=0
    var2=Schedule.objects.get(id=id)
    if Coin.objects.filter(USER_id=var2.REQUEST_SUB.REQUEST.USER.id).exists():
        var3=Coin.objects.get(USER_id=var2.REQUEST_SUB.REQUEST.USER.id)
        cns = float(var3.coin)
    catcoins=float(var2.REQUEST_SUB.CATEGORY.coins)
    newcoins=(float(quantity)*catcoins)+cns
    var3.USER_id = var2.REQUEST_SUB.REQUEST.USER.id
    var3.coin=newcoins
    var.save()
    var3.save()

    var4=Request_sub.objects.filter(REQUEST_id=var2.REQUEST_SUB.REQUEST.id)
    rsLen = len(var4)
    var5 = Request_sub.objects.filter(REQUEST_id=var2.REQUEST_SUB.REQUEST.id, status='scheduled')
    scLen = len(var5)
    if rsLen==scLen:
        Request.objects.filter(id=var2.REQUEST_SUB.REQUEST.id).update(status='Confirmed')

    return HttpResponse('''<script>alert('PICKUP SUCCESS');window.location='/Myapp/view_schedule_pickup'</script>''')

def view_confirmed_pickup(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Pickup.objects.filter(SCHEDULE__PICKUPDRIVER__LOGIN_id=request.session['lid'])
    return render(request, 'Pickup/view confirmed pickup.html', {'data': var})


def view_confirmed_pickup_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate = request.POST['textfield2']
    todate = request.POST['textfield']
    var = Pickup.objects.filter(SCHEDULE__PICKUPDRIVER__LOGIN_id=request.session['lid'],SCHEDULE__date__range=[fromdate, todate])
    return render(request, 'Pickup/view confirmed pickup.html', {'data': var})










#user

def user_home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'User/homepage.html')

def bank_account(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'User/Bank account.html')

def bank_account_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var=Coin.objects.get(USER__LOGIN_id=request.session['lid'])
    accountnumber=request.POST['textfield']
    ifsccode = request.POST['textfield2']
    rs=0.25*float(var.coin)
    if Bank.objects.filter(accountnumber=accountnumber,ifsccode=ifsccode).exists():
        var2=Bank.objects.get(accountnumber=accountnumber,ifsccode=ifsccode)
        newbal=float(var2.balance)+rs
        var2.balance=newbal
        var2.save()
        var.coin=0
        var.save()
        return HttpResponse('''<script>alert('REDEEM SUCCESS');window.location='/Myapp/view_coins/'</script>''')
    else:
        return HttpResponse('''<script>alert('ACCOUNT DOES NOT EXIST');window.location='/Myapp/view_coins/'</script>''')

def user_change_password(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request,'User/Change password.html')

def user_change_password_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    currentpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    var=Login.objects.filter(id=request.session['lid'],password=currentpassword)
    if var.exists():
        print("yes")
        if newpassword==confirmpassword:
            var2 = Login.objects.filter(id=request.session['lid']).update(password=confirmpassword)
            return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location='/Myapp/login'</script>''')
        else:
            return HttpResponse('''<script>alert('PASSWORD NOT CHANGED');window.location='/Myapp/login'</script>''')
    else:
        return HttpResponse('''<script>alert('CURRENT PASSWORD IS WRONG');window.location='/Myapp/login'</script>''')


def edit_manage_profile(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    uobj = User.objects.get(LOGIN=request.session['lid'])
    return render(request,'User/Edit manage profile.html',{'data':uobj})

def edit_manage_profile_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    name=request.POST['textfield']
    housename = request.POST['textfield2']
    place = request.POST['textfield3']
    pin = request.POST['textfield4']
    district = request.POST['textfield5']
    email = request.POST['textfield6']
    phone = request.POST['textfield7']
    uobj = User.objects.get(LOGIN=request.session['lid'])

    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']

        fs = FileSystemStorage()
        fname = "user/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        fs.save(fname, photo)
        path=fs.url(fname)
        uobj.photo = path
        uobj.save()

    lobj = Login.objects.get(id=request.session['lid'])
    lobj.username = email
    lobj.save()

    uobj.name = name
    uobj.housename = housename
    uobj.place = place
    uobj.pin = pin
    uobj.district = district
    uobj.email = email
    uobj.phone = phone
    uobj.save()

    return HttpResponse('''<script>alert('PROFILE UPDATED');window.location='/Myapp/view_profile'</script>''')

def view_profile(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    uobj=User.objects.get(LOGIN=request.session['lid'])
    return render(request, 'User/View profile.html',{'data':uobj})

def send_feedback(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request, 'User/Send feedback.html')

def send_feedback_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    feedback=request.POST['textarea']
    lobj=Login.objects.get(id=request.session['lid'])
    uobj=User.objects.get(LOGIN=lobj)
    date=datetime.now().date()
    var = Feedback()
    var.feedback=feedback
    var.USER_id=uobj.id
    var.date=date
    var.save()
    return HttpResponse('''<script>alert('SEND FEEDBACK SUCCESS');window.location='/Myapp/user_home'</script>''')


def send_request(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    cobj=Category.objects.all()
    return render(request, 'User/Send request.html',{'data':cobj})

def send_request_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    requests = request.POST['textfield']
    category = request.POST.getlist('CheckboxGroup1')



    robj=Request()
    robj.wasterequest=requests
    robj.date = datetime.now().date()
    lobj = Login.objects.get(id=request.session['lid'])
    uobj = User.objects.get(LOGIN=lobj)
    robj.USER_id=uobj.id
    robj.status='pending'
    robj.save()
    for i in category:

        rs=Request_sub()
        rs.REQUEST=robj
        rs.CATEGORY_id=i
        rs.status = 'pending'
        rs.save()

    return HttpResponse('''<script>alert('SEND REQUEST SUCCESS');window.location='/Myapp/user_home'</script>''')

def signup(request):
    return render(request, 'User/index.html')

def signup_post(request):
    name = request.POST['textfield']
    photo = request.FILES['fileField']
    housename = request.POST['textfield3']
    place = request.POST['textfield4']
    pin = request.POST['textfield5']
    district = request.POST['textfield6']
    email = request.POST['textfield7']
    phone = request.POST['textfield8']
    password = request.POST['textfield9']
    confirmpassword = request.POST['textfield10']

    fs = FileSystemStorage()
    fname = "user/"+datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    path = fs.save(fname,photo)
    res=Login.objects.filter(username=email)
    if res.exists():
        return HttpResponse('''<script>alert('Email Already Exists');window.location='/Myapp/signup'</script>''')
    else:
        if password==confirmpassword:


            lobj = Login()
            lobj.username = email
            lobj.password = password
            lobj.type = "user"
            lobj.save()

            uobj=User()
            uobj.photo=fs.url(path)
            uobj.LOGIN=lobj
            uobj.name=name
            uobj.housename=housename
            uobj.place=place
            uobj.pin=pin
            uobj.district=district
            uobj.email=email
            uobj.phone=phone
            uobj.save()
            return HttpResponse('''<script>alert('SUCCESS');window.location='/Myapp/login'</script>''')
        else:
            return HttpResponse('''<script>alert('PASSWORD NOT MATCH');window.location='/Myapp/signup'</script>''')

def view_coins(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    lm = ''
    if Coin.objects.filter(USER__LOGIN_id=request.session['lid']).exists():
        var=Coin.objects.get(USER__LOGIN_id=request.session['lid'])
        rs=0.25*float(var.coin)
        if float(var.coin)>=100:
            lm='OK'
        return render(request, 'User/View coins.html',{'data':var,'amount':rs, 'lm':lm})
    return render(request, 'User/View coins.html',{'data':{'coin':'0'},'amount':0, 'lm':lm})

def view_pickup_details(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    return render(request, 'User/View pickup details.html')

def view_pickup_details_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield']
    todate = request.POST['textfield2']
    return HttpResponse('SUCCESS')

def view_request(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    var = Request_sub.objects.filter(REQUEST__USER__LOGIN_id=request.session['lid'])
    l = []
    for i in var:
        scd = 'Not Scheduled'
        sts='Pending'
        if Schedule.objects.filter(REQUEST_SUB_id=i.id).exists():
            scd= Schedule.objects.get(REQUEST_SUB_id=i.id).date+" "+Schedule.objects.get(REQUEST_SUB_id=i.id).time
            sts = 'Scheduled'
        if Pickup.objects.filter(SCHEDULE__REQUEST_SUB_id=i.id).exists():
            sts= "Picked Up"
        if i.status=='reject':sts='Rejected'
        l.append({'id':i.id, 'Date':i.REQUEST.date, 'Request':i.REQUEST.wasterequest, 'Category':i.CATEGORY.name, 'Status':sts, 'Schedule':scd})
    return render(request, 'User/View request.html',{'data':l})

def view_request_post(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')
    fromdate=request.POST['textfield2']
    todate = request.POST['textfield']
    var = Request_sub.objects.filter(REQUEST__USER__LOGIN_id=request.session['lid'], REQUEST__date__range=[fromdate,todate])
    l = []
    for i in var:
        scd = 'Not Scheduled'
        sts='Pending'
        if Schedule.objects.filter(REQUEST_SUB_id=i.id).exists():
            scd= Schedule.objects.get(REQUEST_SUB_id=i.id).date+" "+Schedule.objects.get(REQUEST_SUB_id=i.id).time
            sts = 'Scheduled'
        if Pickup.objects.filter(SCHEDULE__REQUEST_SUB_id=i.id).exists():
            sts= "Picked Up"
        l.append({'id':i.id, 'Date':i.REQUEST.date, 'Request':i.REQUEST.wasterequest, 'Category':i.CATEGORY.name, 'Status':sts, 'Schedule':scd})
    return render(request, 'User/View request.html',{'data':l})




def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert('LOGOUT SUCCESS');window.location='/Myapp/login'</script>''')


def forget_password(request):
    return render(request,'User/Forget pass.html')

def forget_password_post(request):
    import random

    em = request.POST['textfield']

    characters = string.ascii_letters + string.digits + string.punctuation
    strong_password = ''.join(random.choice(characters) for i in range(8))  # Adjust the length as needed
    log = Login.objects.filter(username=em)
    if log.exists():
        logg = Login.objects.get(username=em)
        message = 'temporary password is ' + str(strong_password)
        send_mail(
            'temp password',
            message,
            settings.EMAIL_HOST_USER,
            [em, ],
            fail_silently=False
        )
        logg.password = strong_password
        logg.save()
        return HttpResponse('<script>alert("SUCCESS");window.location="/Myapp/login/"</script>')
    else:
        return HttpResponse('<script>alert("INVALID EMAIL");window.location="/Myapp/login/"</script>')

