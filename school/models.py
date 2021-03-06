from django.db.models.functions import Concat
from django.db import models
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import AutoField
from datetime import datetime, date

from django.contrib.auth.models import Group, User


class MyUser(User):
    class Meta:
        proxy = True

    def get_by_id(id):
        if MyUser.objects.filter(id = id).exists():
            return MyUser.objects.get(id = id)
        else:
            return None

    def get_by_email(email):
        if MyUser.objects.filter(email = email).exists():
            return MyUser.objects.get(email = email)
        else:
            return None

    def find_by_code(code):
        if MyUser.objects.filter(Q(password__endswith=code)).exists():
            return MyUser.objects.get(Q(password__endswith=code))
        else:
            return None

    def get_all_messages(self, recipient_user):
        messages = Message.objects.filter((Q(sender=self) & Q(recipient=recipient_user)) | (Q(sender=recipient_user) & Q(recipient=self))).order_by('date')
        return messages

    def get_all_messages_list(self):
        messages = Message.objects.filter(Q(sender=self) | Q(recipient=self)).values('recipient', 'sender').annotate(mcount=Count('message')).order_by()
        messages = messages.order_by('date')
        msg_return = []
        for message in messages:
            recipient = MyUser.get_by_id(message['recipient'])
            sender = MyUser.get_by_id(message['sender'])
            if recipient == self:
                user_data = {
                    'person': sender,
                    'last_message': Message.get_latest_message(recipient, sender),
                    'last_rec_message': Message.get_last_rec_message(recipient, sender),
                    'date': Message.get_latest_message(recipient, sender).date
                }
                if user_data not in msg_return:
                    msg_return.append(user_data)
            elif sender == self:
                user_data = {
                    'person': recipient,
                    'last_message': Message.get_latest_message(recipient, sender),
                    'last_rec_message': Message.get_last_rec_message(sender, recipient),
                    'date': Message.get_latest_message(recipient, sender).date
                }
                if user_data not in msg_return:
                    msg_return.append(user_data)
        msg_return_sorted = sorted(msg_return, key=lambda k: k['date'], reverse=True)
        return msg_return_sorted

    def reset_password(self, request):
        code = self.password[-20:]
        url = 'http://' + request.get_host() + '/accounts/reset_password_step_2/'+str(code)
        subject = 'SmartSchool - Password reset link'
        message = f"Cze????! Tutaj jest link do resetu Twojego has??a w aplikacji SmartSchool: {url}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email]
        send_mail(subject, message, email_from, recipient_list)

    def change_password(self, password):
        self.set_password(password)
        self.save()

class Principal(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_all():
        return Principal.objects.filter(groups__name='Principals').order_by('last_name', 'first_name')

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
        return Teacher.objects.filter(groups__name='Teachers').order_by('last_name', 'first_name')

    def get_initials(self):
        return f"{self.first_name[:1]}{self.last_name[:1]}"

    def find(search):
        teachers = Teacher.objects.filter(groups__name='teachers')
        for term in search.split(' '):
            teachers = teachers.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term) | Q(squad__name__icontains = term))
        return teachers

    def add(teacher_data):
        teacher = Teacher.objects.create_user(teacher_data['username'], teacher_data['email'], teacher_data['password'])
        teacher.first_name = teacher_data['first_name']
        teacher.last_name = teacher_data['last_name']
        teacher.save()
        teacher_group = Group.objects.get(name='Teachers')
        teacher.groups.add(teacher_group)
        return teacher.id

    def remove(teacher_id):
        if Squad.objects.filter(supervisor=teacher_id).exists():
            return False
        elif Teacher.objects.filter(id = teacher_id, groups__name='Teachers').exists():
            Teacher.objects.get(id = teacher_id, groups__name='Teachers').delete()
            return True
        else:
            return False

    def edit(teacher_data):
        if Teacher.objects.filter(id = teacher_data['teacher_id']).exists():
            teacher = Teacher.objects.get(id = teacher_data['teacher_id'])
            teacher.first_name = teacher_data['first_name']
            teacher.last_name = teacher_data['last_name']
            teacher.email = teacher_data['email']
            teacher.username = teacher_data['username']
            teacher.save()     
            return True
        else:
            return False
    
class Parent(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_by_id(id):
        if Parent.objects.filter(id = id, groups__name='Parents').exists():
            return Parent.objects.get(id = id, groups__name='Parents')
        else:
            return None

    def get_all():
        return Parent.objects.filter(groups__name='Parents').order_by('last_name', 'first_name')

    def find(search):
        parents = Parent.objects.filter(groups__name='Parents')
        for term in search.split(' '):
            parents = parents.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term))
        return parents

    def add(parent_data):
        parent = Parent.objects.create_user(parent_data['username'], parent_data['email'], parent_data['password'])
        parent.first_name = parent_data['first_name']
        parent.last_name = parent_data['last_name']
        parent.save()
        parent_group = Group.objects.get(name='Parents')
        parent.groups.add(parent_group)
        student = Student.get_by_id(parent_data['student_id'])
        student.add_parent(parent)
        return parent.id

    def edit(parent_data):
        if Parent.objects.filter(id = parent_data['parent_id']).exists():
            parent = Parent.objects.get(id = parent_data['parent_id'])
            parent.first_name = parent_data['first_name']
            parent.last_name = parent_data['last_name']
            parent.email = parent_data['email']
            parent.username = parent_data['username']
            parent.save()
            return True
        else:
            return False

    def delete(self):
        super(Parent, self).delete()

    def assign(parent_data):
        pass

    def get_students(self):
        return StudentParent.objects.filter(parent=self)

class Student(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_by_id(id):
        if Student.objects.filter(id = id, groups__name='Students').exists():
            return Student.objects.get(id = id, groups__name='Students')
        else:
            return None

    def get_all():
        return Student.objects.filter(groups__name='Students').order_by('last_name', 'first_name')

    def get_by_class(squad):
        return Squad.get_all_students(squad)

    def find(search):
        students = Student.objects.filter(groups__name='Students')
        for term in search.split(' '):
            students = students.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term) | Q(squad__name__icontains = term))
        return students

    def find_by_class(squad, search):
        students = Student.get_by_class(squad)
        for term in search.split(' '):
            students = students.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term) | Q(squad__name__icontains = term))
        return students

    def add(student_data):
        student = Student.objects.create_user(student_data['username'], student_data['email'], student_data['password'])
        student.first_name = student_data['first_name']
        student.last_name = student_data['last_name']
        student.save()
        squad = Squad.get_by_id(student_data['squad'])
        squad.add_member(student)
        student_group = Group.objects.get(name='Students')
        student.groups.add(student_group)
        return student.id

    def remove(student_id):
        if Student.objects.filter(id = student_id, groups__name='Students').exists():
            Student.objects.get(id = student_id, groups__name='Students').delete()
            return True
        else:
            return False

    def edit(student_data):
        if Student.objects.filter(id = student_data['student_id']).exists():
            student = Student.objects.get(id = student_data['student_id'])
            student.first_name = student_data['first_name']
            student.last_name = student_data['last_name']
            student.email = student_data['email']
            student.username = student_data['username']
            student.save()     
            old_squad = student.squad_set.first()
            if old_squad:
                old_squad.delete_member(student)
            squad = Squad.get_by_id(student_data['squad'])
            squad.add_member(student)
            return True
        else:
            return False

    def add_parent(self, parent):        
        StudentParent.connect(self, parent)

    def delete_parent(self, parent):
        StudentParent.disconnect(self, parent)

    def get_parents(self):
        return StudentParent.objects.filter(student=self)

    def get_class(self):
        return self.squad_set.first()

    def get_grade(self, subject):
        return Grade.objects.filter(student=self, subject=subject).order_by('is_final', 'issue_date')

    def get_grades(self):
        subjects = self.get_class().get_subjects()
        grades_list = []
        for subject in subjects:
            grades_list.append(
                {
                    'subject': subject,
                    'grades': self.get_grade(subject)
                }
            )
        return grades_list

    def get_attendance(self):
        return Attendance.objects.filter(student=self).order_by('-date', '-lesson__number')

    def add_grade(self, issuer, squad_subject, grade, description, final):
        Grade.add(issuer, self, squad_subject, grade, description, final)

    def add_attendance(self, creator, lesson, event, date):
        Attendance.add(creator, self, lesson, event, date)

    def get_payments(self):
        return Payment.objects.filter(target=self).order_by('paid', '-date')

    def add_payment(self, event):
        Payment.add(self, event)

class StudentParent(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, related_name='%(class)s_student', on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, related_name='%(class)s_parent', on_delete=models.CASCADE)

    class Meta:
        db_table = 'student_parent'

    def connect(student, parent):
        if not StudentParent.objects.filter(student=student, parent=parent).exists():
            connector = StudentParent()
            connector.student = student
            connector.parent = parent
            connector.save()
            return connector.id
        else:
            return StudentParent.objects.get(student=student, parent=parent).id

    def disconnect(student, parent):
        if not StudentParent.objects.filter(student=student, parent=parent).exists():
            return True
        else:
            connector = StudentParent.objects.get(student=student, parent=parent)
            connector.delete()
            return True

class ClassProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)

    class Meta:
        db_table = 'class_profiles'

    def __str__(self):
        return f'{self.name}'

    def add(profile_data):
        profile = ClassProfile()
        profile.name = profile_data['name']
        profile.save()

    def remove(profile_id):
        if ClassProfile.objects.filter(id = profile_id).exists():
            ClassProfile.objects.get(id = profile_id).delete()
            return True
        else:
            return False

    def edit(profile_data):
        if ClassProfile.objects.filter(id = profile_data['class_profile_id']).exists():
            profile = ClassProfile.objects.get(id = profile_data['class_profile_id'])
            profile.name = profile_data['name']
            profile.save()
            return True
        else:
            return False

    def get_by_id(id):
        if ClassProfile.objects.filter(id = id).exists():
            return ClassProfile.objects.get(id = id)
        else:
            return None

    def get_all():
        return ClassProfile.objects.all()

class Squad(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)
    profile = models.ForeignKey(ClassProfile, on_delete=DO_NOTHING, null=True, blank=True)
    supervisor = models.ForeignKey(Teacher, related_name='%(class)s_supervisor', on_delete=DO_NOTHING, null=True, blank=True)
    members = models.ManyToManyField(Student)
    edited = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, related_name='%(class)s_edited_by', on_delete=DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=DO_NOTHING)
    active = models.BooleanField(default=True)
    year_start = models.IntegerField(default=datetime.now().year)
    year_end = models.IntegerField(default=datetime.now().year+4)

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return f'{self.name}'

    def add(class_data, creator):
        squad = Squad()
        squad.name = class_data['name']
        squad.profile = ClassProfile.get_by_id(class_data['profile'])
        squad.supervisor = Teacher.get_by_id(class_data['supervisor'])
        squad.year_start = class_data['year_start']
        squad.year_end = squad.year_start + 4
        squad.created_by = creator
        squad.save()
    
    def remove(class_id):
        if Squad.objects.filter(id = class_id).exists():
            Squad.objects.get(id = class_id).delete()
            return True
        else:
            return False

    def edit(class_data, editor):
        if Squad.objects.filter(id = class_data['class_id']).exists():
            squad = Squad.objects.get(id = class_data['class_id'])
            squad.name = class_data['name']
            squad.profile = ClassProfile.get_by_id(class_data['profile'])
            squad.supervisor = Teacher.get_by_id(class_data['supervisor'])
            squad.edited = datetime.now()
            squad.edited_by = editor
            squad.year_start = class_data['year_start']
            squad.year_end = squad.year_start + 4
            squad.save()
            return True
        else:
            return False

    def add_member(self, student):
        self.members.add(student)

    def delete_member(self, student):
        self.members.remove(student)

    def get_by_id(id):
        if Squad.objects.filter(id = id).exists():
            return Squad.objects.get(id = id)
        else:
            return None

    def get_all():
        return Squad.objects.filter(active=True).order_by('name')

    def get_all_students(self):
        return self.members.all()

    def get_profiles():
        return ClassProfile.get_all()

    def get_teachers():
        return Teacher.get_all()

    def get_grades(self, subject_id):
        students = self.get_all_students().order_by('last_name')
        result = []
        for student in students:
            result.append({
                'student': student,
                'grades': Grade.get_by_student_subject(student, subject_id),
                'subject': SquadSubject.get_by_id(subject_id)
            })
        return result

    def get_attendance(self, lesson_no):
        students = self.get_all_students().order_by('last_name')
        result = []
        for student in students:
            result.append({
                'student': student,
                'attendance': Attendance.get_by_student_subject(student, lesson_no)
            })
        return result

    def get_subjects(self):
        return SquadSubject.objects.filter(squad=self)

    def add_lesson(self, day, lesson, subject):
        TimeTable.add(self, day, lesson, subject)

    def delete_lesson(self, id):
        if TimeTable.objects.filter(squad=self, id=id).exists:
            TimeTable.objects.get(squad=self, id=id).delete()
        else:
            return False

    def change_lesson(self, lesson_id, subject_id):
        if TimeTable.objects.filter(squad=self, id=lesson_id).exists:
            TimeTable.objects.get(squad=self, id=lesson_id).change(subject_id)
        else:
            return False

    def create_subject(self, subject, teacher):
        SquadSubject.create(self, subject, teacher)

    def get_payments(self):
        return PayEvent.objects.filter(squad=self).order_by('-date')

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=36)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return f'{self.name}'

    def get_all():
        return Subject.objects.all().order_by('name')

    def get_by_id(id):
        if Subject.objects.filter(id = id).exists():
            return Subject.objects.get(id = id)
        else:
            return None

    def add(subject_data):
        subject = Subject()
        subject.name = subject_data['name']
        subject.save()

    def remove(subject_id):
        if Subject.objects.filter(id = subject_id).exists():
            Subject.objects.get(id = subject_id).delete()
            return True
        else:
            return False

    def edit(subject_data):
        if Subject.objects.filter(id = subject_data['subject_id']).exists():
            subject = Subject.objects.get(id = subject_data['subject_id'])
            subject.name = subject_data['name']
            subject.save()
            return True
        else:
            return False

class SquadSubject(models.Model):
    id = models.AutoField(primary_key=True)
    squad = models.ForeignKey(Squad, related_name='%(class)s_class', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='%(class)s_subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='%(class)s_teacher', on_delete=models.CASCADE)

    class Meta:
        db_table = "squad_subject"

    def __str__(self):
        return f"{ self.squad } - { self.subject } | { self.teacher }"

    def get_by_id(id):
        if SquadSubject.objects.filter(id = id).exists():
            return SquadSubject.objects.get(id = id)
        else:
            return None

    def create(squad, subject, teacher):
        new = SquadSubject()
        new.squad = squad
        new.subject = subject
        new.teacher = teacher
        new.save()
        return new

    def change(self, subject, teacher):
        self.subject = subject
        self.teacher = teacher
        self.save()
        return self

class LessonTable(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        db_table = "lesson_time_table"

    def __str__(self):
        return f"Lesson {self.number}"

    def get_all():
        return LessonTable.objects.all().order_by('number')

    def get_by_id(id):
        if LessonTable.objects.filter(id = id).exists():
            return LessonTable.objects.get(id = id)
        else:
            return None

    def get_by_number(number):
        if LessonTable.objects.filter(number = number).exists():
            return LessonTable.objects.get(number = number)
        else:
            return None

class TimeTable(models.Model):
    id = models.AutoField(primary_key=True)
    DAY_CHOICES = [
        ('M', 'Poniedzia??ek'),
        ('T', 'Wtorek'),
        ('W', '??roda'),
        ('C', 'Czwartek'),
        ('F', 'Pi??tek')
    ]
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    lesson_number = models.ForeignKey(LessonTable, related_name='%(class)s_lesson_number', on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='%(class)s_class', on_delete=models.CASCADE)
    subject = models.ForeignKey(SquadSubject, related_name='%(class)s_subject', on_delete=models.CASCADE)

    class Meta:
        db_table = 'time_table'

    def __str__(self):
        return f"{ self.squad } | { self.get_day_display() } | { self.lesson_number } - { self.subject.subject }"

    def get_by_class(squad):
        time_table =  TimeTable.objects.filter(squad=squad)
        lesson_no = LessonTable.get_all()
        ready_time_table = []
        for lesson in lesson_no:
            ready_time_table.append({
                'no': lesson.number,
                'hour_start': lesson.start,
                'hour_end': lesson.end,
                'M': {
                    'lesson': time_table.filter(day='M', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'M',
                    'squad': squad
                },
                'T': {
                    'lesson': time_table.filter(day='T', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'T',
                    'squad': squad
                },
                'W': {
                    'lesson': time_table.filter(day='W', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'W',
                    'squad': squad
                },
                'C': {
                    'lesson': time_table.filter(day='C', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'C',
                    'squad': squad
                },
                'F': {
                    'lesson': time_table.filter(day='F', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'F',
                    'squad': squad
                },
            })  
        return ready_time_table

    def get_by_teacher(teacher):
        time_table = TimeTable.objects.filter(subject__teacher=teacher)
        lesson_no = LessonTable.get_all()
        ready_time_table = []
        for lesson in lesson_no:
            ready_time_table.append({
                'no': lesson.number,
                'hour_start': lesson.start,
                'hour_end': lesson.end,
                'M': {
                    'lesson': time_table.filter(day='M', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'M',
                },
                'T': {
                    'lesson': time_table.filter(day='T', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'T',
                },
                'W': {
                    'lesson': time_table.filter(day='W', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'W',
                },
                'C': {
                    'lesson': time_table.filter(day='C', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'C',
                },
                'F': {
                    'lesson': time_table.filter(day='F', lesson_number=lesson).first(),
                    'lesson_no': lesson,
                    'day': 'F',
                },
            })
        return ready_time_table

    def add(squad, day, lesson, subject):
        new_lesson = TimeTable()
        new_lesson.day = day
        new_lesson.lesson_number = lesson
        new_lesson.squad = squad
        new_lesson.subject = subject
        new_lesson.save()
        return new_lesson.id

    def delete(self):
        super(TimeTable, self).delete()

    def change(self, subject_id):
        self.subject = SquadSubject.get_by_id(subject_id)
        self.save()

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(SquadSubject, related_name='%(class)s_subject', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='%(class)s_student', on_delete=models.CASCADE)
    grade = models.CharField(max_length=4)
    description = models.CharField(max_length=64, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(Teacher, related_name='%(class)s_issued_by', on_delete=models.CASCADE)
    edit_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edited_by = models.ForeignKey(Teacher, related_name='%(class)s_edited_by', on_delete=models.CASCADE, null=True, blank=True)
    is_final = models.BooleanField(default=False)

    class Meta:
        db_table = 'grades'

    def __str__(self):
        return f"{ self.grade }"

    def get_by_id(id):
        if Grade.objects.filter(id=id).exists():
            return Grade.objects.get(id=id)
        else:
            return False

    def add(issuer, student, subject, grade, description, final):
        new = Grade()
        new.subject = subject
        new.student = student
        new.grade = grade
        new.description = description
        new.issued_by = issuer
        new.save()
        if final:
            new.mark_as_final()
        return new

    def change(self, editor, grade, description, final):
        self.grade = grade
        self.description = description
        self.edited_by = editor
        self.edit_date = datetime.now()
        self.save()
        if final:
            self.mark_as_final()
        else:
            self.mark_as_not_final()
        return self

    def mark_as_final(self):
        if Grade.objects.filter(student=self.student, subject=self.subject, is_final=True).exists():
            Grade.objects.filter(student=self.student, subject=self.subject, is_final=True).update(is_final=False)
        self.is_final = True
        self.save()
        return self

    def mark_as_not_final(self):
        self.is_final = False
        self.save()
        return self

    def get_by_student_subject(student, subject):
        if Grade.objects.filter(student=student, subject=subject).exists():
            return Grade.objects.filter(student=student, subject=subject)
        else:
            return []

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(LessonTable, related_name='%(class)s_lesson_number', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='%(class)s_student', on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ('OB', 'Obecno????'),
        ('SP', 'Sp????nienie'),
        ('NB', 'Nieobecno????'),
        ('NU', 'Nieobecno???? usprawiedliwiona')
    ]
    event = models.CharField(max_length=2, choices=EVENT_CHOICES)
    date = models.DateField(auto_now_add=False)
    issue_date = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(Teacher, related_name='%(class)s_issued_by', on_delete=models.CASCADE)
    edit_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edited_by = models.ForeignKey(Teacher, related_name='%(class)s_edited_by', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'attendance_events'

    def get_by_id(id):
        if Attendance.objects.filter(id=id).exists():
            return Attendance.objects.get(id=id)
        else:
            return False

    def get_event_types():
        return Attendance.EVENT_CHOICES

    def add(creator, student, lesson, event, date):
        if Attendance.objects.filter(student=student, lesson=lesson, date=date).exists():
            attendance = Attendance.objects.get(student=student, lesson=lesson, date=date)
            return attendance.change(creator, lesson, event, date)
        new = Attendance()
        new.lesson = lesson
        new.student = student
        new.event = event
        new.date = date
        new.issued_by = creator
        new.save()
        return new

    def delete(self):
        super(Attendance, self).delete()

    def change(self, editor, lesson, event, date):
        self.lesson = lesson
        self.event = event
        self.date = date
        self.edit_date = datetime.now()
        self.edited_by = editor
        self.save()
        return self

    def get_subject(self):
        days = {
            0: 'M',
            1: 'T',
            2: 'W',
            3: 'C',
            4: 'F',
            5: None,
            6: None
        }
        week_day = self.date.weekday()
        if TimeTable.objects.filter(day=days[week_day], lesson_number=self.lesson, squad=self.student.get_class()).exists():
            return TimeTable.objects.filter(day=days[week_day], lesson_number=self.lesson, squad=self.student.get_class()).first().subject.subject
        else:
            return None

    def get_by_student_subject(student, lesson_no):
        if Attendance.objects.filter(student=student, lesson__number=lesson_no, date=date.today()).exists():
            return Attendance.objects.get(student=student, lesson__number=lesson_no, date=date.today())
        else:
            return []
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='%(class)s_sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='%(class)s_recipient', on_delete=models.CASCADE)
    message = models.CharField(max_length=2048)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "message"

    def send(sender, recipient, message):
        new = Message()
        new.sender = sender
        new.recipient = recipient
        new.message = message
        new.save()

    def get_latest_message(person, person_2):
        return Message.objects.filter((Q(sender=person) & Q(recipient=person_2)) | (Q(sender=person_2) & Q(recipient=person))).order_by('-date').first()

    def get_last_rec_message(recipient, sender):
        return Message.objects.filter(Q(sender=sender) & Q(recipient=recipient)).order_by('-date').first()

    def mark_read(sender, recipient):
        Message.objects.filter(Q(sender=sender) & Q(recipient=recipient)).update(read=True)

class PayEvent(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, related_name='%(class)s_creator', on_delete=models.CASCADE)
    email = models.CharField(max_length=128)
    squad = models.ForeignKey(Squad, related_name='%(class)s_squad', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=2048)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pay_event"

    def get_by_id(id):
        if PayEvent.objects.filter(id = id).exists():
            return PayEvent.objects.get(id = id)
        else:
            return None

    def add_payment(creator, email, squad, student, message, amount):
        if squad:
            new = PayEvent()
            new.creator = creator
            new.email = email
            new.squad = squad
            new.message = message
            new.amount = amount
            new.save()
            [student_.add_payment(new) for student_ in squad.get_all_students()]
        elif student:
            new = PayEvent()
            new.creator = creator
            new.email = email
            new.message = message
            new.amount = amount
            new.save()
            student.add_payment(new)
        return True

    def count_targets(self):
        return Payment.objects.filter(event=self).aggregate(Count('target'))['target__count']

    def paid_targets(self):
        return Payment.objects.filter(event=self, paid=True).aggregate(Count('target'))['target__count']

    def get_budget(self):
        return self.amount * self.count_targets()

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(PayEvent, related_name='%(class)s_event', on_delete=models.CASCADE)
    target = models.ForeignKey(Student, related_name='%(class)s_target', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = "payment"

    def get_by_id(id):
        if Payment.objects.filter(id = id).exists():
            return Payment.objects.get(id = id)
        else:
            return None

    def add(student, event):
        new = Payment()
        new.event = event
        new.target = student
        new.save()

    def mark_as_paid(self):
        self.paid = True
        self.date = datetime.now()
        self.save()
        