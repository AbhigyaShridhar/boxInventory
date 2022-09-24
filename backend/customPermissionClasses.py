from cgitb import lookup
from operator import length_hint
from urllib import request
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import BoxSerializer
from .models import Box, User

class IsAuthenticatedAndIsStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        #if the request is for read only attributes
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return request.user.is_staff

class IsAuthenticatedIsStaffAndIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.user == obj.created_by

def filterQueryset(queryset, filters):
    if 'length_less' in filters:
        queryset = queryset.filter(length__lte=filters['length_less'])
    if 'length_more' in filters:
        queryset = queryset.filter(length__gte=filters['length_more'])
    if 'breadth_less' in filters:
        queryset = queryset.filter(length__lte=filters['breadth_less'])
    if 'breadth_more' in filters:
        queryset = queryset.filter(breadth__gte=filters['breadth_more'])
    if 'height_less' in filters:
        queryset = queryset.filter(breadth__lte=filters['height_less'])
    if 'height_more' in filters:
        queryset = queryset.filter(height__gte=filters['height_more'])
    if 'volume_more' in filters:
        queryset = queryset.filter(volume__gte=filters['volume_more'])
    if 'volume_less' in filters:
        queryset = queryset.filter(volume__lte=filters['volume_less'])
    if 'area_more' in filters:
        queryset = queryset.filter(area__gte=filters['area_more'])
    if 'area_less' in filters:
        queryset = queryset.filter(area__lte=filters['area_less'])
    if 'after' in filters:
        queryset = queryset.filter(created_at__gte=filters['after'])
    if 'before' in filters:
        queryset = queryset.filter(created_at__lte=filters['before'])
    if 'creator' in filters:
        try:
            queryset = queryset.filter(created_by=User.objects.get(username=filters['creator']))
        except User.DoesNotExist:
            queryset = []
    return queryset

class BoxCreateViewUpdate(APIView):
    serializer_class = BoxSerializer
    queryset = Box.objects.all()
    permission_classes = [IsAuthenticatedAndIsStaff]

    def get_queryset(self):
        request = self.request
        filters = request.GET
        if len(filters) > 0:
            queryset = self.queryset.all()
            queryset = filterQueryset(queryset, filters)
            return queryset
        return self.queryset.all()

class BoxesOfUser(BoxCreateViewUpdate):
    permission_classes = [IsAuthenticatedIsStaffAndIsOwner]

    def get_queryset(self):
        request = self.request
        filters = request.GET
        if len(filters) > 0:
            user = request.user
            queryset = self.queryset.all().filter(created_by=user)
            queryset = filterQueryset(queryset, filters)
            return queryset
        return self.queryset.all()