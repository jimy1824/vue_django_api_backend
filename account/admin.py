from django.contrib import admin
from django import forms
from .models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'is_active', 'first_name', 'last_name', 'gender', 'email')
    list_display_links = ('first_name', 'last_name', 'email',)
    search_fields = ('id', 'first_name', 'email')
    ordering = ['-id', ]

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(User, AccountAdmin)
