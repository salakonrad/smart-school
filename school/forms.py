from django import forms
from django.db.models.fields import IntegerField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=48, label="Nazwa użytkownika")
    password = forms.CharField(max_length=64, label="Hasło")

class ResetPasswordForm(forms.Form):
    email = forms.CharField(max_length=75)

class ResetPassword2Form(forms.Form):
    user_id = forms.IntegerField()
    password = forms.CharField(max_length=64)


# Classes

class AddSquadForm(forms.Form):
    name = forms.CharField(max_length=36)
    profile = forms.IntegerField()
    supervisor = forms.IntegerField()
    year_start = forms.IntegerField()

class DeleteSquadForm(forms.Form):
    class_id = forms.IntegerField()

class ChangeSquadForm(forms.Form):
    class_id = forms.IntegerField()
    name = forms.CharField(max_length=36)
    profile = forms.IntegerField()
    supervisor = forms.IntegerField()
    year_start = forms.IntegerField()


# Class subjects

class AddClassSubjectForm(forms.Form):
    squad_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    subject_id = forms.IntegerField()

class DeleteClassSubjectForm(forms.Form):
    squad_subject_id = forms.IntegerField()

class ChangeClassSubjectForm(forms.Form):
    squad_subject_id = forms.IntegerField()
    squad_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    subject_id = forms.IntegerField()


# Class profiles

class AddProfileForm(forms.Form):
    name = forms.CharField(max_length=36)

class DeleteProfileForm(forms.Form):
    class_profile_id = forms.IntegerField()

class ChangeProfileForm(forms.Form):
    class_profile_id = forms.IntegerField()
    name = forms.CharField(max_length=36)


# Subjects

class AddSubjectForm(forms.Form):
    name = forms.CharField(max_length=36)

class DeleteSubjectForm(forms.Form):
    subject_id = forms.IntegerField()

class ChangeSubjectForm(forms.Form):
    subject_id = forms.IntegerField()
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


# Teachers

class AddTeacherForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)

class DeleteTeacherForm(forms.Form):
    teacher_id = forms.IntegerField()

class ChangeTeacherForm(forms.Form):
    teacher_id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)


# Parents

class AddParentForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)
    student_id = forms.IntegerField()

class DeleteParentForm(forms.Form):
    parent_id = forms.IntegerField()

class AssignParentForm(forms.Form):
    student_id = forms.IntegerField()
    parent_id = forms.IntegerField()
    next = forms.CharField(max_length=512)

class ChangeParentForm(forms.Form):
    parent_id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.CharField(required=False)


# Users

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=512)
    new_password = forms.CharField(max_length=512)

class RandomPasswordForm(forms.Form):
    user_id = forms.IntegerField()


# Time Tables

class AddLessonForm(forms.Form):
    day = forms.CharField(max_length=1)
    lesson_id = forms.IntegerField()
    squad_id = forms.IntegerField()
    subject_id = forms.IntegerField()

class DeleteLessonForm(forms.Form):
    time_table_id = forms.IntegerField()
    squad_id = forms.IntegerField()

class ChangeLessonForm(forms.Form):
    time_table_id = forms.IntegerField()
    squad_id = forms.IntegerField()
    subject_id = forms.IntegerField()


# Grades

class AddGradeForm(forms.Form):
    student_id = forms.IntegerField()
    subject_id = forms.IntegerField()
    grade = forms.CharField(max_length=4)
    description = forms.CharField(max_length=64, required=False)
    final = forms.BooleanField(required=False)

class DeleteGradeForm(forms.Form):
    grade_id = forms.IntegerField()

class ChangeGradeForm(forms.Form):
    grade_id = forms.IntegerField()
    grade = forms.CharField(max_length=4)
    description = forms.CharField(max_length=64, required=False)
    final = forms.BooleanField(required=False)


# Attendance

class AddAttendanceForm(forms.Form):
    student_id = forms.IntegerField()
    lesson_id = forms.IntegerField()
    event = forms.CharField(max_length=2)
    date = forms.DateField()

class DeleteAttendanceForm(forms.Form):
    attendance_id = forms.IntegerField()

class ChangeAttendanceForm(forms.Form):
    attendance_id = forms.IntegerField()
    lesson_id = forms.IntegerField()
    event = forms.CharField(max_length=2)
    date = forms.DateField()


# Messages

class NewMessageForm(forms.Form):
    sender_id = forms.IntegerField()
    recipient_id = forms.IntegerField()
    message = forms.CharField(max_length=2048)


# Payment

class AddPaymentForm(forms.Form):
    student_id = forms.IntegerField(required=False)
    squad_id = forms.IntegerField(required=False)
    email = forms.CharField(max_length=128)
    amount = forms.DecimalField(max_digits=5, decimal_places=2)
    message = forms.CharField(max_length=2048, required=False)

class PayForm(forms.Form):
    payment_id = forms.IntegerField(required=False)

class DeletePaymentForm(forms.Form):
    payment_id = forms.IntegerField(required=False)
    event_id = forms.IntegerField(required=False)