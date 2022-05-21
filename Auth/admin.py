from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from Core.models import *
from import_export.admin import ImportExportModelAdmin
from multiupload.fields import MultiFileField
from django.forms import ModelForm
from import_export.fields import Field
from import_export import resources


User = get_user_model()

# class StudentImageResource(resources.ModelResource):
#     class Meta:
#         model = StudentImage
#         fields = ('image',)

class LateEntryResource(resources.ModelResource):
    student_number = Field()
    student_name = Field()
    venue = Field()
    late_count = Field()
    class Meta:
        model = LateEntry
        fields = ('timestamp',)
    
    def dehydrate_student_number(self, instance):
        return instance.student.st_no
    
    def dehydrate_student_name(self, instance):
        return instance.student.name
    
    def dehydrate_venue(self, instance):
        return instance.venue
    
    def dehydrate_late_count(self, instance):
        return instance.student.late_entry.all().count()

class LateEntryAdmin(ImportExportModelAdmin):
    resource_class = LateEntryResource
    # readonly_fields = ('timestamp',)
    # list_display = ('student', 'venue')
    # search_fields = ('student', 'venue')
    # list_filter = ('timestamp',)

# class StudentImageAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = StudentImageResource

class ImageForm(ModelForm):
    additional_images = MultiFileField(min_num=1,required=False)

    class Meta:
        model = Batch
        fields = "__all__"

    def save(self, commit=True): # It may be better to do that in  save_m2m for newly created objects
        save = super().save(commit)
        try:
            for image in self.cleaned_data["additional_images"]:
                    saved_image = StudentImage(batch=save, image=image)
                    saved_image.save()
        except ValueError:
            return ValidationError("First Create a Batch then upload the Images")
        return save


class StudentImageAdmin(admin.StackedInline):
    model = StudentImage

class BatchAdmin(admin.ModelAdmin):
    form = ImageForm
    inlines = [StudentImageAdmin]

class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    ordering = ['id']
    list_display = ['email','id', 'name']
    list_filter = ['is_active','is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login',)}),
        # ('Group Permissions', {
        #     'classes': ('collapse',),
        #     'fields': ('groups', 'user_permissions', )
        # })
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    # # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(StudentImage)
admin.site.register(LateEntry, LateEntryAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Branch)
admin.site.register(Venue)
