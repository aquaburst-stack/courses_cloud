from django.contrib import admin
from module.models import ContactUs
# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'message')


admin.site.register(ContactUs, ContactUsAdmin)