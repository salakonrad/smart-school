from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import AutoField

from django.contrib.auth.models import User


class Principal(User):
    class Meta:
        proxy = True

class Teacher(User):
    class Meta:
        proxy = True

class Parent(User):
    class Meta:
        proxy = True

class Student(User):
    class Meta:
        proxy = True

class ClassProfile(models.Model):
    class_profile = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)

    class Meta:
        db_table = 'class_profiles'

    def __str__(self):
        return f'{self.name}'

class Squad(models.Model):
    squad = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)
    profile = models.ForeignKey(ClassProfile, on_delete=DO_NOTHING, null=True, blank=True)
    supervisor = models.ForeignKey(Teacher, related_name='%(class)s_supervisor', on_delete=DO_NOTHING, null=True, blank=True)
    edited = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, related_name='%(class)s_edited_by', on_delete=DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=DO_NOTHING)

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return f'{self.name}'

