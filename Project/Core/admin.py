from django.contrib import admin
from django.contrib.auth.models import Group
from Core.models import *

# Register your models here.
from django.contrib import admin


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

staff_login.register(Student)
staff_login.register(Branch)
staff_login.register(Year)
staff_login.register(LateEntry)
