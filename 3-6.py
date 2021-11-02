Creamos un archvio llamado serializer,
que se va a encargar de pasar de objeto de BBDD a json
y tambien de tomar el json y pasarlo a la BBDD


#---------- serializer.py----------------------
from rest_framework import serializers #importamos
from .models import Users


class Users_Serializer(serializers.ModelSerializer):#este en especifico cumple simple funcion de 
                                                    #acoplarse al modelo
       class Meta(): #esto si o si
             model=Users #especificamos el modelo
             fields="__all__"  #le ponemos todos los campos sino en lista
                               #los que queramos


#----------------views.py-------------------------------------

from rest_framework.decorators import api_view #importamos el decorador
from rest_framework.response import Response #importamos el Response


from .models import Users
from .serializers import Users_Serializer

#este decorador(api_view) nos permite hacer las respuestas en modo api,
# especificando que metodos aceptamos(pueden ser varios)

#con el serializer convertimos en json los objetos.
#cuando metemos data hay que verificar .is_valid()
#cuando solicictamos informacion no hay que verificar nada

@api_view(["GET"]) 
def all_users(request):

    users=Users.objects.all()
    serialized_users=Users_Serializer(users,many=True) #convertimos en json los objetos. Como son varios hay que ppner many=True

    return Response(serialized_users.data)


@api_view(["POST"])
def new_user(request):
    new_user=Users_Serializer(data=request.data)# AL poner data le estamos diciendo que haga uno nuevo

    if new_user.is_valid(): #verificamos que todos los campos se cumplan como deben ser
        new_user.save() #salvamos
        return Response(new_user.data)
    
    else:
        return Response(new_user.errors)

@api_view(["GET"])
def specify_user(request,pk):
    filtred_user=Users.objects.get(id=pk)

    serialized_user=Users_Serializer(filtred_user,many=False)

    return Response(serialized_user.data)

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




#------------urls.py-----------------
from django.urls import path
from hello import views


urlpatterns=[
             path("all/",views.all_users),
             path("filter/<str:pk>/",views.specify_user),
             path("update/<str:pk>/",views.update_user),
             path("delete/<str:pk>/",views.delete_user),
             path("new/",views.new_user)

]