from django import forms
from django.db.models.fields import IntegerField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=48, label="Nazwa użytkownika")
    password = forms.CharField(max_length=64, label="Hasło")


# Classes

class AddSquadForm(forms.Form):
    name = forms.CharField(max_length=36)
    profile = forms.IntegerField()
    supervisor = forms.IntegerField()

class DeleteSquadForm(forms.Form):
    class_id = forms.IntegerField()

class ChangeSquadForm(forms.Form):
    class_id = forms.IntegerField()
    name = forms.CharField(max_length=36)
    profile = forms.IntegerField()
    supervisor = forms.IntegerField()


# Class profiles

class AddProfileForm(forms.Form):
    name = forms.CharField(max_length=36)

class DeleteProfileForm(forms.Form):
    class_profile_id = forms.IntegerField()

class ChangeProfileForm(forms.Form):
    class_profile_id = forms.IntegerField()
    name = forms.CharField(max_length=36)


# Students

class AddStudentForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)
    squad = forms.IntegerField()

class DeleteStudentForm(forms.Form):
    student_id = forms.IntegerField()

class ChangeStudentForm(forms.Form):
    student_id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)
    squad = forms.IntegerField()


# Parents

class AddParentForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)
    student_id = forms.IntegerField()

class ChangeParentForm(forms.Form):
    parent_id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)