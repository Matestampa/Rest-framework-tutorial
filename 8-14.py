#clase 8-14  como funciona serializer-----------------------------------

#------------serializers-py--------------------------------------------------------------
class Test_user_serializer(serializers.Serializer):
      username=serializers.CharField(max_length=20)
      email=serializers.EmailField()

      #todas estas validate se van a ejecutar cuando hagamos is.valid() (ver all_users view)
      
      def validate_username(self,value):#en cada funcion validate_{campo} podemos tratar por individual cualquiera
          if len(value)>20:
                raise serializers.ValidationError("Muy corto") #esto se va a ver cuando en la view
                                                               #si no pasa el is_valid()
                                                               #hacemos print(instance.errors)
      
      def validate_email(self,value):
          print(value)
      
      
      def create(self,validated_data):#Cuando luego del is.valid() hacemos save, esto es lo que hace para crear algo nuevo
                                      #aca lo ponemos manualmente, pero en realidad lo sacaria del modelos que pusimos
                                      #en la clase Meta
          
          return Users.objects.create(**validated_data)
          
          #----password------------
          new_user=Users.objects.create(**validated_data)#creamos un nuevo usuario y despues modifucamos el atributo especifico de password
          new_user.password=new_user.encrypt_pswd(validated_data["password"])#le agregue una funcion propia en la clase del modelo
          new_user.save() #salvamos
          
          return new_user


      def update(self,instance,validated_data): #para actualizar empieza a recoorrer cada campo, que haya en el model
                                                #que hayamos puwsto en la meta, y empieza a actualizar
          instance.name=validated_data.get("name")
          instance.email=validated_data.get("email")

          instance.save()
          return instance

          #-------password---------------
          updated_user=super().update(instance,validated_data) #automatizamos
          updated_user.password=updated_user.encrypt_pswd(validated_data["password"])#hacemos lo mismo que en create
          updated_user.save()
          return updated_user
      


      def save(self):#save es el que desencadena create, o update, dependiendo si le pasamos una instancia o no
                     #podemos sobreescribirlo para que por ej. No queremos guardar la info, pero si queremos
                     #mandarla por mail.
          
          send_mail(self.validated_data)#este validated data ya lo adquiere la clase en los validate

          #entonces aca al reescribirlo estariamos anulando la llamada que era automatica a create o update
      
      def to_representation(self, instance):#esto es como genera el json(cuando hacemos el .data)
                                            #la ventaja de sobreescribir es que podemos devolver solo los campps que
                                            #queramos y les podemos czmbiar el nombre a las claves.
                                            #ppr defecto el serializer devolveria todos los campos que hayamos puesto en fields en Meta
          
          return {
                   "username":instance.username,
                   "correo":instance.email,
          }


#----------views-------------------------------------------------------------------

@api_view(["GET"]) 
def all_users(request):
    
    users=Users.objects.all()

    #-------------test--------------------------------------#este apartado lo hicimos para hacer pruebas
                                                            #si bien la funcion esta hecha para get
                                                            #el apartado lo usamos como post para probar lo de los errores
    test_data={
                "username":"emikel", #solo utilizamos estos dos campos, los cuales especificamos que tendria el serializer de prueba
                "email":"tutte@gmail.com"
    }

    test_user=Test_user_serializer(data=test_data)

    if test_user.is_valid():
        print("paso validaciones")
    
    else:
        print(test_user.errors) #solo se muestran los errorres si los imprimimos
                                #sino hay error pero no se muestarn en especifico
        
    #------------------------------------------------------------------------
    
    return Response(serialized_users.data,status=status.HTTP_200_OK)



@api_view(["POST"])
def new_user(request):
    #new_user=Users_Serializer(data=request.data)# AL poner data le estamos diciendo que haga uno nuevo
    new_user=Test_user_serializer(data=request.data)
    
    if new_user.is_valid(): 
        new_user.save()
        return Response({"message":"usuario creado correctamente"},status=status.HTTP_201_CREATED)
    
    else:
        return Response(new_user.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def update_user(request,pk):
    
    filtred_user=Users.objects.get(id=pk)

    updated_user=Test_user_serializer(instance=filtred_user,data=request.data)

    if updated_user.is_valid():
        updated_user.save()
        return Response(updated_user.data)
    
    else:
        return Response(updated_user.errors)

