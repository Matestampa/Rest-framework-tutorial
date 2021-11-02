from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Users
from .serializers import Users_Serializer,Test_user_serializer



@api_view(["GET"]) #este api view nos permite hacer las respuestas en modo api, especificando que metodos aceptamos(puedne ser varios)
def all_users(request):
    
    users=Users.objects.all()
    serialized_users=Users_Serializer(users,many=True) #convertimos en json los objetos. Como son varios hay que ppner many=True
    
    #-------------test--------------------------------------
    test_data={
                "username":"emikel",
                "email":"tutte@gmail.com"
    }

    test_user=Test_user_serializer(data=test_data)

    if test_user.is_valid():
        print("paso validaciones")
    
    else:
        print(test_user.errors)#si no ponemos print no salen los errores
        
    #-----------------------------------------------
    
    return Response(serialized_users.data,status=status.HTTP_200_OK)






@api_view(["POST"])
def new_user(request):
    new_user=Users_Serializer(data=request.data)# AL poner data le estamos diciendo que haga uno nuevo

    if new_user.is_valid(): #verificamos que todos los campos se cumplan como deben ser
        new_user.save() #salvamos
        return Response({"message":"usuario creado correctamente"},status=status.HTTP_201_CREATED)
    
    else:
        return Response(new_user.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def specify_user(request,pk):
    filtred_user=Users.objects.get(id=pk)
    
    if filtred_user:
       serialized_user=Users_Serializer(filtred_user,many=False)

       return Response(serialized_user.data,status=status.HTTP_200_OK)
    
    else:
        return Response({"message":"No se encontro el usuario"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def update_user(request,pk):
    
    filtred_user=Users.objects.get(id=pk)

    updated_user=Users_Serializer(instance=filtred_user,data=request.data)#al ponerle la instancia sabe que dbe reemplazar con lo que hay en data

    if updated_user.is_valid():#otra vez verificamos
        updated_user.save()
        return Response(updated_user.data)
    
    else:
        return Repsonse(updated_user.errors)


@api_view(["DELETE"])
def delete_user(request,pk):
    filtred_user=Users.objects.get(id=pk)

    filtred_user.delete()

    return Response("Deleted")
