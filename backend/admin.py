from django.contrib import admin
from .models import *

# Register your models here.
class BoxInLine(admin.StackedInline):
    model = Box
    fk_name = 'created_by'
    readonly_fields = ('created_by', )

class UserAdmin(admin.ModelAdmin):
    inlines = [BoxInLine]

admin.site.register(User, UserAdmin)
admin.site.register(Box)