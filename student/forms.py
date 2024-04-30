from django import forms
from student.models import Student, User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Password'}))


class UserStudentForm(forms.ModelForm):
    # Additional fields for the User model
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = Student
        fields = ['date_of_birth', 'address', 'city_town', 'country', 'photo']

    def save(self, commit=True):
        # Save the user
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Save the student related to the user
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
    

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Last Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Password'}))


    class Meta:
        model = Student
        fields = ['date_of_birth', 'address', 'city_town', 'country', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control my-2', 'placeholder': 'Date of Birth'}),
            'address': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Address'}),
            'city_town': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Country'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file my-2', 'placeholder': 'Photo', 'accept': 'image/png, image/jpeg, image/jpg'}),
        }
    

    def __init__(self, *args, **kwargs):
        # Extract user data from the associated Student instance
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            if instance.user:
                initial['first_name'] = instance.user.first_name
                initial['last_name'] = instance.user.last_name
                initial['email'] = instance.user.email
                initial['username'] = instance.user.username
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the user
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Save the student related to the user
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
