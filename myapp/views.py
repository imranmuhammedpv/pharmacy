from django.shortcuts import render,redirect
from .models import phar
from .models import user,product,booking,cart
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


def userpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1=user.objects.get(id=userid)
        return render(request, 'user/userhome.html', {'data2': use1})


def pharpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1 = phar.objects.get(id=userid)
        return render(request, 'pharmacy/pharmacyhome.html',{'data3': use1})

def regform(request):
    if request.method=='POST':
        name=request.POST['name']
        address=request.POST['address']
        email= request.POST['email']
        password=request.POST['password']
        data1=user.objects.create(name=name,address=address,password=password,email=email,type=0)
        data1.save()
        return render(request,'lognew.html')
    else:
        return render(request,'signnew.html')



def log(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            data2=user.objects.get(name=username)
            if data2.type == 0 and password==data2.password:
                request.session['id']=data2.id
                return redirect(userpage)
            else:
                return HttpResponse("password error")
        except user.DoesNotExist :
            data3 = phar.objects.get(name=username, password=password)
            if data3.entry=='APPROVED':
                request.session['id']=data3.id
                return redirect(pharpage)
            else:
                return HttpResponse("admin approval ")
        except Exception as e:
            return HttpResponse("password invalid")
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
              data7 =user.objects.get(id=data6)
              if newpsw==conpsw:
                  if data7.password==currentpsw:
                      data7.password=newpsw
                      data7.save()
                      context = {
                          'message': 'password change successfully'
                      }
                      return render(request, 'user/userhome.html', context)

                  else:
                   return HttpResponse("password does not match")
              else:
                 return HttpResponse(" password error")
           except Exception:
                return HttpResponse(" error")
    else:
     return redirect(log)



def editprofile(request,id):
    if 'id' in request.session:
        use1 = user.objects.get(id=id)
        userpr = editprofileform(instance=use1)
        if request.method=='POST':
            userpr=editprofileform(request.POST,instance=use1)
            if userpr.is_valid():
                userpr.save()
                return redirect(log)
        else:
          return render(request,'user/editprofile.html',{'form':userpr,'user':use1})
    else:
        return redirect(log)


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
        use2 = product.objects.get(id=id)
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






def editpharmacyprofile(request,id):
    if 'id' in request.session:
        use1 = phar.objects.get(id=id)
        userpr1 = pharmacyprofileform(instance=use1)
        if request.method=='POST':
            userpr1=pharmacyprofileform(request.POST,instance=use1)
            if userpr1.is_valid():
                userpr1.save()
                return redirect(log)
        else:
          return render(request,'pharmacy/pharmacyeditprofile.html',{'form1':userpr1,'user1':use1})
    else:
        return redirect(log)


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
        user1 =user.objects.get(id=userid)

        currentmedicine=product.objects.get(id=id)
        if booking.objects.filter(medicinename=currentmedicine,name=user1).exists():
            return redirect(already)
        else:
            data=booking.objects.create(name=user1,medicinename=currentmedicine)
            data.save()
            return render(request,'user/booksuccess.html')

def Add_cart (request,id):
    if 'id' in request.session:
        useid=request.session['id']
        user2=user.objects.get(id=useid)
        medicine=product.objects.get(id=id)
        if cart.objects.filter(medicineid=medicine,userid=user2).exists():
            return redirect(alreadycart)
        else:
            data6 = cart.objects.create(userid=user2,medicineid=medicine)
            data6.save()
            data = cart.objects.filter(userid=user2)
            return render(request,'user/cartpage.html',{'cartt':data})
    else:
        return redirect(log)
def cartdelete(request,id):
    if 'id' in request.session:
        useid = request.session['id']
        user2 = user.objects.get(id=useid)
        data1=cart.objects.get(medicineid=id,userid=user2)
        print(data1)
        data1.delete()
        data = cart.objects.filter(userid=user2)
        return render(request, 'user/cartpage.html', {'cartt': data})
    else:
        return redirect(log)


def alreadycart(request):
    return render(request,'user/cartalready.html')

def history (request):
    if 'id' in request.session:
        useid=request.session['id']
        user1=user.objects.get(id=useid)
        history=booking.objects.filter(name=user1)
        return render(request, 'user/history.html', {'hist': history})
    else:
        return redirect(log)


def phar_history(request):
    data5=booking.objects.all()
    return render(request,'pharmacy/history.html',{'result':data5})

def view_cart(request):
    if 'id' in request.session:
        use1=request.session['id']
        use2=user.objects.get(id=use1)
        view=cart.objects.filter(userid=use2)
        return render(request,'user/viewcart.html',{'view':view})
def paymentt(request,id):
    if 'id' in request.session:
        use1=request.session['id']
        use2=user.objects.get(id=use1)
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


