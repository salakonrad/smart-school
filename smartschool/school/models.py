from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import AutoField
from datetime import datetime

from django.contrib.auth.models import User


class Principal(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Teacher(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_by_id(id):
        if Teacher.objects.filter(id = id).exists():
            return Teacher.objects.get(id = id)
        else:
            return None

    def get_all():
        return Teacher.objects.filter(groups__name='Teachers')

class Parent(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Student(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class ClassProfile(models.Model):
    class_profile = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)

    class Meta:
        db_table = 'class_profiles'

    def __str__(self):
        return f'{self.name}'

    def get_by_id(id):
        if ClassProfile.objects.filter(class_profile = id).exists():
            return ClassProfile.objects.get(class_profile = id)
        else:
            return None

    def get_all():
        return ClassProfile.objects.all()

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

    def add(class_data, creator):
        squad = Squad()
        squad.name = class_data['name']
        squad.profile = ClassProfile.get_by_id(class_data['profile'])
        squad.supervisor = Teacher.get_by_id(class_data['supervisor'])
        squad.created_by = creator
        squad.save()
    
    def remove(class_id):
        if Squad.objects.filter(squad = class_id).exists():
            Squad.objects.get(squad = class_id).delete()
            return True
        else:
            return False

    def edit(class_data, editor):
        if Squad.objects.filter(squad = class_data['class_id']).exists():
            squad = Squad.objects.get(squad = class_data['class_id'])
            squad.name = class_data['name']
            squad.profile = ClassProfile.get_by_id(class_data['profile'])
            squad.supervisor = Teacher.get_by_id(class_data['supervisor'])
            squad.edited = datetime.now()
            squad.edited_by = editor
            squad.save()
            return True
        else:
            return False

    def get_all():
        return Squad.objects.all().order_by('name')

    def get_profiles():
        return ClassProfile.get_all()

    def get_teachers():
        return Teacher.get_all()

