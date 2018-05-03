from django.contrib import admin
from .models import Employee, GroupProxy
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class EmployeeChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Employee


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + ('job_title',)


class EmployeeAdmin(UserAdmin):
    model = Employee
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm

    list_display = ('full_name', 'username', 'is_staff')
    list_filter = ('job_title',) + UserAdmin.list_filter
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('job_title',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'job_title'),
        }),
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(Group)
admin.site.register(GroupProxy, GroupAdmin)
