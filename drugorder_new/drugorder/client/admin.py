from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .models import Order,Drug,Wish_List,Product,Shopping_Cart,Wish_To_Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _

admin.site.register(Shopping_Cart)
admin.site.register(Order)
admin.site.register(Drug)
admin.site.register(Wish_List)
admin.site.register(Product)
admin.site.register(Wish_To_Order)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# class UserCreationFormExtended(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationFormExtended, self).__init__(*args, **kwargs)
#         self.fields[Profile.user_type] = forms.CharField(label=_("user_type"))

class CustomUserAdmin(UserAdmin):
    # UserAdmin.add_form = UserCreationFormExtended
    # UserAdmin.add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('user_type', 'username', 'password1', 'password2',)
    #     }),
    # )
    inlines = (ProfileInline, )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)