from django.contrib import admin
from student.models import Student
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    # Exclude permission-related fields from the admin form
    exclude = ("groups", "user_permissions")


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'address', 'city_town', 'country', 'photo')
    # list_filter = ('availability', 'category')
    search_fields = ('address', 'city_town', 'country')

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)