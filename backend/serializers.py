from email import message
from venv import create
from rest_framework import serializers
from .models import *
from django.db.models import Avg
from rest_framework.validators import ValidationError
from django.conf import settings
import datetime

class userSerializer(serializers.ModelSerializer):
    creator_of = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'creator_of']
        read_only_fields = ['is_staff', 'creator_of']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class BoxSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True
    )

    class Meta:
        model = Box
        fields = '__all__'
        read_only_fields = ['updated_at']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request", None)
        if not (request and request.user and request.user.is_staff):
            fields.pop('created_by')
            fields.pop('updated_at')
        return fields
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        length = validated_data['length']
        breadth = validated_data['breadth']
        height = validated_data['height']
        volume = length * breadth * height
        area = 2 * (length * breadth + length * height + breadth * height)
        box = Box.objects.create(created_by=user, height=height, length=length, breadth=breadth, area=area, volume=volume)
        box.save()
        flag, message = self.manuallyValidate()
        if not flag:
            box.delete()
            raise ValidationError(message)
        return box
    
    def update(self, instance, validated_data):
        length = instance.length
        breadth = instance.breadth
        height = instance.height
        prev = instance
        if 'length' in validated_data:
            length = validated_data['length']
        if 'breadh' in validated_data:
            length = validated_data['breadh']
        if 'height' in validated_data:
            length = validated_data['height']
        volume = length * breadth * height
        area = 2 * (length * breadth + length * height + breadth * height)
        instance.height = height
        instance.breadth = breadth
        instance.length = length
        instance.volume = volume
        instance.area = area
        instance.save()
        flag, message = self.manuallyValidate()
        if not flag:
            instance = prev
            instance.save()
            raise ValidationError(message)
        return instance

    def manuallyValidate(self):
        request = self.context['request']
        user = request.user
        d = datetime.datetime.today()
        sunday_offset = (d.weekday() - 6) % 7
        sunday = d - datetime.timedelta(days = sunday_offset)
        Boxes = Box.objects.filter(created_at__gte=sunday)
        countBoxes = Boxes.count()
        Boxes = Boxes.filter(created_by=user)
        countUsersBoxes = Boxes.count()
        if countBoxes >= settings.L1:
            return False, "max limit for user reached"
        elif countUsersBoxes >= settings.L2:
            return False, "max weekly limit reached"
        Boxes = Box.objects.filter(created_by=user)
        if Boxes.count() > 0:
            avVolume = Boxes.aggregate(Avg('volume'))['volume__avg']
            avArea = Boxes.aggregate(Avg('area'))['area__avg']
            if avVolume > settings.V1:
                return False, "max average volume exceeded"
            elif avArea > settings.A1:
                return False, "max average area exceeded"
        return True, "valid"
