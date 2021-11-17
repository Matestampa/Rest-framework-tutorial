from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Users
from .serializers import Users_Serializer,Test_user_serializer



#esta clases estan preparadas para recibir de tipo get y devuelven listas de cosas

class GeneralListAPIView(generics.ListAPIView): #hacemos una general para la parte de devolver
      

      def get_queryset(self):
          model=self.get_serializer().Meta.model
          return model.objects.all()


class UsersListAPIView(GeneralListAPIView):#en cada particular solo tendriamos que poner el serializer_class, si heredamos de la de arriba
      serializer_class=Users_Serializer