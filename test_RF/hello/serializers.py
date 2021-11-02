from rest_framework import serializers
from .models import Users


class Users_Serializer(serializers.ModelSerializer):
       class Meta():
             model=Users
             fields="__all__"



#clase 8-11  como funciona serializer-----------------------------------
class Test_user_serializer(serializers.Serializer):
      username=serializers.CharField(max_length=20)
      email=serializers.EmailField()

      def validate_username(self,value):#en cada funcion validate_{campo} podemos tratar por individual cualquiera
          if len(value)>2:
                raise serializers.ValidationError("Muy corto")
      
      def validate_email(self,value):
          print(value)
      

      def create(self,validated_data):
          pass


      def update(self,validated_data):
          pass