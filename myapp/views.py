from django.shortcuts import render,redirect
from .models import Pharmacy
from .models import user,product,booking,cart,Login
from django.shortcuts import HttpResponse
from .forms import editprofileform
from .forms import pharmacyprofileform
from .forms import editproductform

from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
        return render(request,'user/userhome.html')
def store(request):
    data = product.objects.all()
    return render(request, 'user/store.html', {'data': data})
def registration (request):
    return render(request,'signnew.html')
def pharmacyreg(request):
    return render(request,'pharmacy/pharsign.html')

def userpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1=Login.objects.get(id=userid)
        return render(request, 'user/userhome.html', {'data2': use1})
    else:
        return HttpResponse('invalid')


def pharpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1 = Login.objects.get(id=userid)
        return render(request, 'pharmacy/pharmacyhome.html',{'data3': use1})
    else:
        return HttpResponse("invalid")



def regform(request):
    if request.method=='POST':
        name=request.POST['name']
        address= request.POST['address']
        email= request.POST['email']
        password=request.POST['password']
        phone_no = request.POST['phone_no']
        login=Login.objects.create(username=name,password=password,type="user",status="APPROVED")
        login.save()
        # logindata=Login.objects.get(id=login.id)
        data1=user.objects.create(name=name,address=address,email=email,phone_no=phone_no,loginid=login)
        data1.save()
        return render(request,'lognew.html')
    else:
        return render(request,'signnew.html')
def pharmacyregform(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_no=request.POST['phone_no']
        address=request.POST['address']
        password=request.POST['password']
        login = Login.objects.create(username=name, password=password, type="pharmacy")
        login.save()
        data2=Pharmacy.objects.create(name=name,email=email,address=address,phone_no=phone_no,loginid=login)
        data2.save()
        return render(request, 'lognew.html')
    else:
        return render(request, 'pharmacy/pharsign.html')





def log(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            data=Login.objects.get(username=username,password=password)
            if data.type == "user" and data.status=='APPROVED' :
                request.session['id']=data.id
                return redirect(userpage)
            elif data.type =="pharmacy" and data.status=='APPROVED':
                request.session['id'] = data.id
                return redirect(pharpage)
            else:
                return HttpResponse("admin approval ")

        except Exception as e:
            return HttpResponse(e)
    else:
        return render(request,'lognew.html')






def logout(request):
     if 'id' in request.session:
         request.session.flush()
         return redirect(log)


def changepsw(request):
    return render(request,'user/changepsw.html')





def changepassword(request):
    if 'id' in request.session:
        data6=request.session['id']
        if request.method == "POST":
           currentpsw = request.POST['cpsw']
           newpsw=request.POST['npsw']
           conpsw = request.POST['cnpsw']
           try:
              data7 =Login.objects.get(id=data6)
              if newpsw==conpsw:
                      data7.password=newpsw
                      data7.save()
                      context = {
                          'message': 'password change successfully'
                      }
                      return render(request, 'user/userhome.html', context)
              else:
                 return HttpResponse(" password does not match")
           except Exception:
                return HttpResponse(" error")
    else:
     return redirect(log)

def editprofile(request):
    if 'id' in request.session:
        user_id = request.session['id']
        data = Login.objects.get(id=user_id)
        userdata = user.objects.get(loginid=data)
        if request.method=='POST':
            newname = request.POST['newname']
            newemail = request.POST['newemail']
            newaddres = request.POST['newaddress']
            newphone_no = request.POST['newphone_no']
            print(userdata)
            print(data)
            userdata.name = newname
            userdata.email = newemail
            userdata.adress = newaddres
            userdata.phone_no = newphone_no
            data.username= newname
            userdata.save()
            data.save()
            return redirect(userpage)
        else:
            return render(request, 'user/editprofile.html', {'data': userdata})

    else:
        return redirect(log)



# def editprofile(request,id):
#     if 'id' in request.session:
#         use1 = Login.objects.get(id=id)
#         userdata=user.objects.get(loginid=use1)
#         userpr = editprofileform(instance=userdata)
#         if request.method=='POST':
#             userpr=editprofileform(request.POST,instance=userdata)
#             if userpr.is_valid():
#                 userpr.save()
#                 return redirect(log)
#         else:
#           return render(request,'user/editprofile.html',{'form':userpr,'user':use1})
#     else:
#         return redirect(log)


def addproduct(request):
    if request.method=='POST':
        image=request.FILES['image']
        medicinename=request.POST['medicinename']
        price=request.POST['price']
        company=request.POST['company']
        type=request.POST['type']
        data=product.objects.create(image=image,medicinename=medicinename,price=price,company=company,type=type)
        data.save()
        return redirect(viewproduct)


def viewproduct(request):
    data=product.objects.all()
    return render(request,'pharmacy/viewproduct.html',{'data':data})





# def editproduct(request,id):
#     data1=product.objects.get(id=id)
#     if request.method=='POST':
#      newmedicinename=request.POST['newmedicinename']
#      newprice=request.POST['newprice']
#      newimage=request.POST['mewimage']
#
#      try:
#          data1=product.objects.get(id=id)
#          data1.medicinename =newmedicinename
#          data1.price =newprice
#          data1.image =newimage
#          data1.save()
#          return redirect(viewproduct)
#      except Exception:
#          return HttpResponse("check the name")
#
#     else:
#         return render(request,'pharmacy/editproduct.html')


def editproductt(request,id):
    if 'id' in request.session:
        use2 = product.  objects.get(id=id)
        print(use2)
        userpr2 = editproductform(instance=use2)
        if request.method=='POST':
            userpr2=editproductform(request.POST,request.FILES,instance=use2)
            if userpr2.is_valid():
                userpr2.save()
                return redirect(viewproduct)
        else:
            return render(request,'pharmacy/editproduct.html',{'form2':userpr2,'user1':use2})
    else:
        return redirect(viewproduct)

def deleteproduct(request,id):
    data=product.objects.get(id=id)
    data.delete()
    return redirect(viewproduct)

def editpharmacyprofile(request):
    if 'id' in request.session:
        use_id =request.session['id']
        data=Login.objects.get(id=use_id)
        userdata=Pharmacy.objects.get(loginid=data)
        if request.method == 'POST':
            newshopname=request.POST['newshopname']
            newemail=request.POST['newemail']
            newaddress=request.POST['newemail']
            newphone_no=request.POST['newphone_no']
            print(userdata)
            print(data)
            userdata.name=newshopname
            userdata.adress=newaddress
            userdata.email=newemail
            userdata.phone_no=newphone_no
            data.username=newshopname
            userdata.save()
            data.save()
            return redirect(pharpage)
        else:
            return render(request, 'pharmacy/pharmacyeditprofile.html', {'data':userdata})
    else:
        return redirect(log)






# def editpharmacyprofile(request,id):
#     if 'id' in request.session:
#         use1 = Login.objects.get(id=id)
#         userpr1 = pharmacyprofileform(instance=use1)
#         if request.method=='POST':
#             userpr1=pharmacyprofileform(request.POST,instance=use1)
#             if userpr1.is_valid():
#                 userpr1.save()
#                 return redirect(log)
#         else:
#           return render(request,'pharmacy/pharmacyeditprofile.html',{'form1':userpr1,'user1':use1})
#     else:
#         return redirect(log)


def book(request,id):
    if 'id' in request.session:
        data7=product.objects.get(id=id)
        return render(request,'user/book.html',{'medicine':data7})




def succsess(request):
    return render(request,'user/booksuccess.html')
def already(request):
    return render(request,'user/alreadybooked.html')


def buymedicine(request,id):
    if 'id' in request.session:
        userid=request.session['id']
        user1 =Login.objects.get(id=userid)
        userdata=user.objects.get(loginid=user1)
        currentmedicine=product.objects.get(id=id)
        if booking.objects.filter(medicinename=currentmedicine,name=userdata).exists():
            return redirect(already)
        else:
            data=booking.objects.create(name=userdata,medicinename=currentmedicine)
            data.save()
            return render(request,'user/booksuccess.html')

def Add_cart (request,id):
    if 'id' in request.session:
        useid=request.session['id']
        user2=Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user2)
        medicine=product.objects.get(id=id)
        if cart.objects.filter(medicineid=medicine,userid=userdata).exists():
            return redirect(alreadycart)
        else:
            data6 = cart.objects.create(userid=userdata,medicineid=medicine)
            data6.save()
            data = cart.objects.filter(userid=userdata)
            return render(request,'user/cartpage.html',{'cartt':data})
    else:
        return redirect(log)
def cartdelete(request,id):
    if 'id' in request.session:
        useid = request.session['id']
        user2 = Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user2)
        data1=cart.objects.get(medicineid=id,userid=userdata)
        print(data1)
        data1.delete()
        data = cart.objects.filter(userid=userdata)
        return render(request, 'user/cartpage.html', {'cartt': data})
    else:
        return redirect(log)


def alreadycart(request):
    return render(request,'user/cartalready.html')

def history (request):
    if 'id' in request.session:
        useid=request.session['id']
        user1=Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user1)
        history=booking.objects.filter(name=userdata)
        return render(request, 'user/history.html', {'hist': history})
    else:
        return redirect(log)


def phar_history(request):
    data5=booking.objects.all()
    return render(request,'pharmacy/history.html',{'result':data5})

def view_cart(request):
    if 'id' in request.session:
        use1=request.session['id']
        use2=Login.objects.get(id=use1)
        userdata = user.objects.get(loginid=use2)
        view=cart.objects.filter(userid=userdata)
        return render(request,'user/viewcart.html',{'view':view})
def paymentt(request,id):
    if 'id' in request.session:
        use1=request.session['id']
        use2=Login.objects.get(id=use1)
        book=product.objects.get(id=id)
        return render(request,'user/payment.html',{'book':book})



def searchbar(request):
    if request.method=='GET':
        result=request.GET.get('search')
        if result:
            products = product.objects.all().filter(medicinename=result)
            return render(request,'user/searchresult.html',{'products':products})
        else:
            print("no information to show")
            return render(request,'user/searchresult.html',{})


