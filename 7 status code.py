#importamos los codigos de status
from rest_framework import status

@api_view(["GET"]) 
def all_users(request):

    users=Users.objects.all()
    serialized_users=Users_Serializer(users,many=True) 

    return Response(serialized_users.data,status=status.HTTP_200_OK)
    #como todo fue bien le ponemos el 200




@api_view(["POST"])
def new_user(request):
    new_user=Users_Serializer(data=request.data)

    if new_user.is_valid(): 
        new_user.save() 
        #si todo esta bien devolvemos mensaje y codigo 200, o 201
        return Response({"message":"usuario creado correctamente"},status=status.HTTP_201_CREATED)
        
    else:
        #si va mal usamos el error que tre el serializer y el codigo 400
        return Response(new_user.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def specify_user(request,pk):
    filtred_user=Users.objects.get(id=pk)
    
    if filtred_user: #si encontramos un usuario con ese id
       serialized_user=Users_Serializer(filtred_user,many=False)

       return Response(serialized_user.data,status=status.HTTP_200_OK)
    
    else:
        #si no lo encontramos mandamos un mensaje especifico y codigo 400
        return Response({"message":"No se encontro el usuario"},status=status.HTTP_400_BAD_REQUEST)