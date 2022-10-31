from re import T
from django.shortcuts import render
from django.urls import is_valid_path
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from reminder.models import Todos
from reminder.serializer import TodoSerializer,RegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import permissions,authentication
# Create your views here.

class TodosVew(ViewSet):
    def list(self,request,*args,**kw):
        qq=Todos.objects.all()
        serializer=TodoSerializer(qq,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qq=Todos.objects.get(id=id)
        serializer=TodoSerializer(qq,many=False)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
         n_id=kw.get("pk")
         Todos.objects.get(id=n_id).delete()
         return Response(data="deleted")

    def update(self,request,*args,**kw):
        m_id=kw.get("pk")
        obj=Todos.objects.get(id=m_id)
        serializer=TodoSerializer(data=request.data,instance=obj) 
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TodoModelViewset(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.BasicAuthentication]

    def create(self, request, *args, **kw):
        Serializer=TodoSerializer(data=request.data)
        if Serializer.is_valid():
            Todos.objects.create(**Serializer.validated_data,user=request.user)
            return Response(data=Serializer.data)
        else:
            return Response(data=Serializer.errors)
    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        qp=TodoSerializer(qs,many=True)
        return Response(data=qp.data)

    @action(methods=["GET"],detail=False)
    def completed_tods(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        qs=TodoSerializer(qs,many=True)
        return Response(data=qs.data)

    @action(methods=["GET"],detail=True)    
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)

class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    def list(self,request,*args,**kw):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data) 
      # def create(self,request,*args,**kw):
    #     serialiser=RegistrationSerializer(data=request.data)
    #     if serialiser.is_valid():
    #         User.objects.create_user(**serialiser._validated_data)##
    #         return Response(data=serialiser.data)
    #     else:
    #         return Response(data=serialiser.errors)
    #nfnhfff





        
