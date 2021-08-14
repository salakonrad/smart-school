from django.db.models.functions import Concat
from django.db import models
from django.db.models import Q
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import AutoField
from datetime import datetime

from django.contrib.auth.models import Group, User


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
        if Teacher.objects.filter(id = teacher_id, groups__name='Teachers').exists():
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
        return f'{self.last_name} {self.first_name}'

    def get_by_id(id):
        if Student.objects.filter(id = id, groups__name='Students').exists():
            return Student.objects.get(id = id, groups__name='Students')
        else:
            return None

    def get_all():
        return Student.objects.filter(groups__name='Students').order_by('last_name', 'first_name')

    def find(search):
        students = Student.objects.filter(groups__name='Students')
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
    year_end = models.IntegerField(default=datetime.now().year+1)

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
        squad.year_end = squad.year_start + 1
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

    def get_profiles():
        return ClassProfile.get_all()

    def get_teachers():
        return Teacher.get_all()

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

class TimeTable(models.Model):
    id = models.AutoField(primary_key=True)
    DAY_CHOICES = [
        ('M', 'Poniedziałek'),
        ('T', 'Wtorek'),
        ('W', 'Środa'),
        ('C', 'Czwartek'),
        ('F', 'Piątek')
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
    squad = models.ForeignKey(Squad, related_name='%(class)s_class', on_delete=models.CASCADE)
    subject = models.ForeignKey(SquadSubject, related_name='%(class)s_subject', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='%(class)s_student', on_delete=models.CASCADE)
    grade = models.CharField(max_length=4)
    description = models.CharField(max_length=64, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grades'

    def __str__(self):
        return f"{ self.grade }"