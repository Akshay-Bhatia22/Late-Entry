from django.contrib import admin
from django.contrib.auth.models import Group
from Core.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from Core.forms import OperatorCreationForm



# Register your models here.
from django.contrib import admin

class StaffUserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','id', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'groups')}),
        (('Personal Info'), {'fields': ('name',)}),
        (('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ('groups',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','password1', 'password2')
        }),
    )
    add_form = OperatorCreationForm

    def get_queryset(self, request):
        qs = super(StaffUserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(Q(is_superuser=False) & Q(is_staff=False))
        return qs


class StaffAdminArea(admin.AdminSite):
    """An Admin Panel for the Staff Admin. With the ability to manage Late Entry Students.
        and list/add Operators"""
    site_header = "Staff's Login"

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["app_list"] = admin.AdminSite.get_app_list(self, request)
        return super(StaffAdminArea, self).index(request, extra_context)


staff_login = StaffAdminArea(name="StaffAdmin")

staff_login.register(Operator, StaffUserAdmin)
staff_login.register(Student)
staff_login.register(Branch)
staff_login.register(Year)
staff_login.register(LateEntry)
staff_login.register(Venue)

