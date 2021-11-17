from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Users
from .serializers import Users_Serializer,Test_user_serializer



@api_view(["GET"]) 
def all_users(request):
    
    users=Users.objects.all()
    serialized_users=Users_Serializer(users,many=True) 

    #-------------test--------------------------------------
    test_data={
                "username":"emikel",
                "email":"tutte@gmail.com"
    }

    test_user=Test_user_serializer(data=test_data)

    if test_user.is_valid():
        print("paso validaciones")
    
    else:
        print(test_user.errors)
        
    #-----------------------------------------------
    
    return Response(serialized_users.data,status=status.HTTP_200_OK)






@api_view(["POST"])
def new_user(request):
    new_user=Users_Serializer(data=request.data)
    
    if new_user.is_valid(): 
        new_user.save()
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

    updated_user=Users_Serializer(instance=filtred_user,data=request.data)

    if updated_user.is_valid():
        updated_user.save()
        return Response(updated_user.data)
    
    else:
        return Response(updated_user.errors)


@api_view(["DELETE"])
def delete_user(request,pk):
    filtred_user=Users.objects.get(id=pk)

    filtred_user.delete()

    return Response("Deleted")
