from django.db import models

# Create your models here.



class Users(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    ubicacion=models.CharField(max_length=50)

    
    def encrypt_pswd(self,text):
        return text+" esmikel"

    def __str__(self):
        return f"{self.id} : {self.username}"