from django.db import models

# Create your models here.


class ContactUs(models.Model):
    email = models.EmailField(db_column='email')
    subject = models.CharField(max_length=255, null=True, blank=True, db_column='subject')
    message = models.TextField(db_column='message', null=True, blank=True)

    class Meta:
        db_table = 'ContactUs'
        ordering = ['-id']


class Course(models.Model):
    name = models.CharField(verbose_name='Course Name', max_length=100, db_column='course_name')
    description = models.TextField(db_column='course_description', verbose_name='Course Description')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Course'



AVAILABILITY_CHOICES = {
    "Open": "Open",
    "Closed": "Closed"
}

class Module(models.Model):
    name = models.CharField(max_length=150, db_column='name', verbose_name='Name')
    code = models.CharField(max_length=20, db_column='code', verbose_name='Code', unique=True)
    credit = models.PositiveIntegerField(db_column='credit', verbose_name='Credit')
    category = models.CharField(max_length=50, db_column='category', verbose_name='Category')
    description = models.TextField(db_column='description', verbose_name='Description')
    availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='Open')
    courses = models.ManyToManyField("Course", related_name='modules', db_column='courses', verbose_name='Courses')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Module'


class Registration(models.Model):
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} registered for {self.module.name} on {self.registration_date}"

    class Meta:
        db_table = 'Registration'
        unique_together = ('student', 'module')
        ordering = ['-registration_date']