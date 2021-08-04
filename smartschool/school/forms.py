from django import forms
from django.db.models.fields import IntegerField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=48, label="Nazwa użytkownika")
    password = forms.CharField(max_length=64, label="Hasło")

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