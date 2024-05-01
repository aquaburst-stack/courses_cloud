from django.contrib import admin
from module.models import ContactUs, Course, Module, Registration
# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'message')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category', 'description', 'availability', 'custom_method')
    list_filter = ['availability']
    search_fields = ('name', 'code', 'credit', 'category', 'description')

    def custom_method(self, obj):
        return ", ".join([related_obj.name for related_obj in obj.courses.all()])


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'registration_date')



admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Registration, RegistrationAdmin)