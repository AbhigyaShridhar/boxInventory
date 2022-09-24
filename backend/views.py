from venv import create
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import permissions
from .serializers import *
from .models import *
from .customPermissionClasses import *

# Create your views here.
def index(request):
    return HttpResponse("hello world")

class Register(generics.CreateAPIView):
    serializer_class = userSerializer
    queryset = User.objects.all()

class UserDetails(generics.RetrieveAPIView):
    serializer_class = userSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateBox(BoxCreateViewUpdate, generics.CreateAPIView):
    pass

class UpdateBox(BoxCreateViewUpdate, generics.UpdateAPIView):
    pass

class DeleteBox(BoxesOfUser, generics.DestroyAPIView):
    pass

class ListBoxes(BoxCreateViewUpdate, generics.ListAPIView):
    pass

class ListUserBoxes(BoxesOfUser, generics.ListAPIView):
    pass