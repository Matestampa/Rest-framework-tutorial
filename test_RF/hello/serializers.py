from rest_framework import fields, serializers

from .models import Users


class Users_Serializer(serializers.ModelSerializer):
       class Meta():
             model=Users
             fields="__all__"



#clase 8-11  como funciona serializer-----------------------------------
class Test_user_serializer(serializers.ModelSerializer):
      
      class Meta():
            model=Users
            fields="__all__"
      
      
      def create(self,validated_data):
          #----password------------
          new_user=Users.objects.create(**validated_data)#creamos un nuevo usuario y despues modifucamos el atributo especifico de password
          new_user.password=new_user.encrypt_pswd(validated_data["password"])#le agregue una funcion propia en la clase del modelo
          new_user.save() #salvamos
          
          return new_user


      def update(self,instance,validated_data): 
          #-------password---------------
          updated_user=super().update(instance,validated_data)
          updated_user.password=updated_user.encrypt_pswd(validated_data["password"])
          updated_user.save()
          return updated_user