from django.db import models

# Create your models here.
class phar (models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    phone_no=models.IntegerField()
    password=models.CharField(max_length=15)
    status=(('APPROVED','APPROVED'),
            ('PENDING','PENDING'),
            ('REJECT','REJECT')
            )
    entry=models.CharField(choices=status,max_length=20,default='PENDING')

    def __str__(self):
        return self.name

class user (models.Model):
    name=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    email=models.CharField(max_length=25)
    password=models.CharField(max_length=10)

    type=models.IntegerField()

    def __str__(self):
        return self.name

class product(models.Model):
    image=models.FileField()
    medicinename=models.CharField(max_length=20)
    price=models.CharField(max_length=20)
    company=models.CharField(max_length=20)
    type=models.CharField(max_length=10)


    def __str__(self):
        return self.medicinename

class booking(models.Model):
    name=models.ForeignKey(user,on_delete=models.CASCADE)
    medicinename=models.ForeignKey(product,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True,blank=True)



    def __str__(self):
        return self.medicinename.medicinename

class cart(models.Model):
    medicineid=models.ForeignKey(product,on_delete=models.CASCADE)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)

    def __str__(self):
        return self.medicineid.medicinename
