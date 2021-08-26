from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import *
from .models import *


# /
def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    return render(request, 'auth/login.html')


# /accounts/login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'auth/login.html', {'status': 'noauth'})
        else:
            return render(request, 'auth/login.html', {'status': 'invalidform', 'error': form.errors})
    else:
        return render(request, 'auth/login.html')


# /accounts/logout
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


# /classes
@login_required
@permission_required('school.view_squad', raise_exception=True)
def class_list_view(request, error_message=None):
    data = {
        'classes': Squad.get_all(),
        'profiles': Squad.get_profiles(),
        'teachers': Squad.get_teachers(),
        'errors': error_message
    }
    return render(request, 'class/class_list.html', {'data': data})


# /classes/add
@login_required
@permission_required('school.add_squad', raise_exception=True)
def class_add(request):
    if request.method == 'POST':
        form = AddSquadForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            class_profile = form.cleaned_data['profile']
            class_supervisor = form.cleaned_data['supervisor']
            class_start_year = form.cleaned_data['year_start']
            Squad.add({
                'name': class_name,
                'profile': class_profile,
                'supervisor': class_supervisor,
                'year_start': class_start_year
            }, request.user)
            return HttpResponseRedirect('/classes')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /classes/delete
@login_required
@permission_required('school.delete_squad', raise_exception=True)
def class_delete(request):
    if request.method == 'POST':
        form = DeleteSquadForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            Squad.remove(class_id)
            return HttpResponseRedirect('/classes')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /classes/change
@login_required
@permission_required('school.change_squad', raise_exception=True)
def class_change(request):
    if request.method == 'POST':
        form = ChangeSquadForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            class_name = form.cleaned_data['name']
            class_profile = form.cleaned_data['profile']
            class_supervisor = form.cleaned_data['supervisor']
            class_start_year = form.cleaned_data['year_start']
            Squad.edit({
                'class_id': class_id,
                'name': class_name,
                'profile': class_profile,
                'supervisor': class_supervisor,
                'year_start': class_start_year
            }, request.user)
            return HttpResponseRedirect('/classes')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /class_profiles
@login_required
@permission_required('school.view_classprofile', raise_exception=True)
def class_profile_list_view(request, error_message=None):
    data = {
        'class_profiles': Squad.get_profiles(),
        'errors': error_message
    }
    return render(request, 'class/class_profiles.html', {'data': data})


# /class_profiles/add
@login_required
@permission_required('school.add_classprofile', raise_exception=True)
def class_profile_add(request, error_message=None):
    if request.method == 'POST':
        form = AddProfileForm(request.POST)
        if form.is_valid():
            profile_name = form.cleaned_data['name']
            ClassProfile.add({
                'name': profile_name
            })
            return HttpResponseRedirect('/class_profile')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /class_profiles/delete
@login_required
@permission_required('school.delete_classprofile', raise_exception=True)
def class_profile_delete(request, error_message=None):
    if request.method == 'POST':
        form = DeleteProfileForm(request.POST)
        if form.is_valid():
            profile_id = form.cleaned_data['class_profile_id']
            ClassProfile.remove(profile_id)
            return HttpResponseRedirect('/class_profile')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /class_profiles/change
@login_required
@permission_required('school.change_classprofile', raise_exception=True)
def class_profile_change(request, error_message=None):
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            profile_id = form.cleaned_data['class_profile_id']
            profile_name = form.cleaned_data['name']
            ClassProfile.edit({
                'class_profile_id': profile_id,
                'name': profile_name
            })
            return HttpResponseRedirect('/class_profile')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)


# /class_subject/class/id
@login_required
@permission_required('school.view_squadsubject', raise_exception=True)
def class_subject_list_view(request, id):
    squad = Squad.get_by_id(id)
    data = {
        'squad': squad,
        'class_subjects': squad.get_subjects(),
        'subjects': Subject.get_all(),
        'teachers': Teacher.get_all()
    }
    return render(request, 'class/class_subjects.html', {'data': data})


# /class_subjects/add
@login_required
@permission_required('school.add_squadsubject', raise_exception=True)
def class_subject_add(request):
    if request.method == 'POST':
        form = AddClassSubjectForm(request.POST)
        if form.is_valid():
            squad = Squad.get_by_id(form.cleaned_data['squad_id'])
            squad.create_subject(*[
                Subject.get_by_id(form.cleaned_data['subject_id']),
                Teacher.get_by_id(form.cleaned_data['teacher_id'])
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /class_subjects/delete
@login_required
@permission_required('school.delete_squadsubject', raise_exception=True)
def class_subject_delete(request):
    if request.method == 'POST':
        form = DeleteClassSubjectForm(request.POST)
        if form.is_valid():
            squad_subject = SquadSubject.get_by_id(form.cleaned_data['squad_subject_id'])
            squad_subject.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /class_subjects/change
@login_required
@permission_required('school.change_squadsubject', raise_exception=True)
def class_subject_change(request):
    if request.method == 'POST':
        form = ChangeClassSubjectForm(request.POST)
        if form.is_valid():
            squad_subject = SquadSubject.get_by_id(form.cleaned_data['squad_subject_id'])
            squad_subject.change(*[
                Subject.get_by_id(form.cleaned_data['subject_id']),
                Teacher.get_by_id(form.cleaned_data['teacher_id'])
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /subjects
@login_required
@permission_required('school.view_subject', raise_exception=True)
def subject_list_view(request):
    data = {
        'subjects': Subject.get_all()
    }
    return render(request, 'class/subjects.html', {'data': data})


# /subjects/add
@login_required
@permission_required('school.add_subject', raise_exception=True)
def subject_add(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['name']
            Subject.add({
                'name': subject_name
            })
            return HttpResponseRedirect('/subjects')
        else:
            return subject_list_view(request)
    else:
        return subject_list_view(request)


# /subjects/delete
@login_required
@permission_required('school.delete_subject', raise_exception=True)
def subject_delete(request):
    if request.method == 'POST':
        form = DeleteSubjectForm(request.POST)
        if form.is_valid():
            subject_id = form.cleaned_data['subject_id']
            Subject.remove(subject_id)
            return HttpResponseRedirect('/subjects')
        else:
            return subject_list_view(request)
    else:
        return subject_list_view(request)


# /subjects/change
@login_required
@permission_required('school.change_subject', raise_exception=True)
def subject_change(request):
    if request.method == 'POST':
        form = ChangeSubjectForm(request.POST)
        if form.is_valid():
            subject_id = form.cleaned_data['subject_id']
            subject_name = form.cleaned_data['name']
            Subject.edit({
                'subject_id': subject_id,
                'name': subject_name
            })
            return HttpResponseRedirect('/subjects')
        else:
            return subject_list_view(request)
    else:
        return subject_list_view(request)


# /students
@login_required
@permission_required('school.view_student', raise_exception=True)
def student_list_view(request, error_message=None):
    # Search
    if request.GET.get('search'):
        students_list = Student.find(request.GET.get('search'))
    else:
        students_list = Student.get_all()

    # Paginator
    paginator = Paginator(students_list, 10)
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    students_page = paginator.get_page(page_number)
    paginator = {
        'actual_page': page_number,
        'has_next': students_page.has_next(),
        'has_prev': students_page.has_previous()
    }
    if paginator['has_next']: 
        paginator['next_page'] = students_page.next_page_number()
    if paginator['has_prev']: 
        paginator['prev_page'] = students_page.previous_page_number()

    data = {
        'students': students_page,
        'classes': Squad.get_all(),
        'paginator': paginator,
        'error': error_message
    }
    return render(request, 'users/student_list.html', {'data': data})


# /students/details/id
@login_required
@permission_required('school.view_student', raise_exception=True)
def student_view(request, id, error_message=None):
    student = Student.get_by_id(id)
    data = {
        'student': student,
        'parents': student.get_parents(),
        'classes': Squad.get_all(),
        'parents_list': Parent.get_all(),
        'error': error_message
    }
    return render(request, 'users/student.html', {'data': data})


# /students/add
@login_required
@permission_required('school.add_student', raise_exception=True)
def student_add(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            if Student.objects.filter(username=form.cleaned_data['username']).exists():
                return student_list_view(request, 'username')
            student_id = Student.add({
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'squad': form.cleaned_data['squad']
            })
            return HttpResponseRedirect(f'/students/details/{student_id}')
        else:
            return student_list_view(request)
    else:
        return student_list_view(request)


# /students/delete
@login_required
@permission_required('school.delete_student', raise_exception=True)
def student_delete(request):
    if request.method == 'POST':
        form = DeleteStudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            Student.remove(student_id)
            return HttpResponseRedirect('/students')
        else:
            return student_list_view(request)
    else:
        return student_list_view(request)


# /students/change
@login_required
@permission_required('school.change_student', raise_exception=True)
def student_change(request):
    if request.method == 'POST':
        form = ChangeStudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = Student.get_by_id(student_id)
            if student.username != form.cleaned_data['username']:
                if Student.objects.filter(username=form.cleaned_data['username']).exists():
                    return student_view(request, student_id, 'username')
            Student.edit({
                'student_id': student_id,
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'squad': form.cleaned_data['squad']
            })
            return HttpResponseRedirect(f'/students/details/{student_id}')
        else:
            return student_view(request, form.cleaned_data['student_id'])
    else:
        return student_list_view(request)


# /teachers
@login_required
@permission_required('school.view_teacher', raise_exception=True)
def teacher_list_view(request, error_message=None):
    # Search
    if request.GET.get('search'):
        teachers_list = Teacher.find(request.GET.get('search'))
    else:
        teachers_list = Teacher.get_all()

    # Paginator
    paginator = Paginator(teachers_list, 10)
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    teachers_page = paginator.get_page(page_number)
    paginator = {
        'actual_page': page_number,
        'has_next': teachers_page.has_next(),
        'has_prev': teachers_page.has_previous()
    }
    if paginator['has_next']: 
        paginator['next_page'] = teachers_page.next_page_number()
    if paginator['has_prev']: 
        paginator['prev_page'] = teachers_page.previous_page_number()

    data = {
        'teachers': teachers_page,
        'paginator': paginator,
        'error': error_message
    }
    return render(request, 'users/teacher_list.html', {'data': data})


# /teachers/details/id
@login_required
@permission_required('school.view_teacher', raise_exception=True)
def teacher_view(request, id, error_message=None):
    teacher = Teacher.get_by_id(id)
    data = {
        'teacher': teacher,
        'error': error_message
    }
    return render(request, 'users/teacher.html', {'data': data})


# /teachers/add
@login_required
@permission_required('school.add_teacher', raise_exception=True)
def teacher_add(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            if Teacher.objects.filter(username=form.cleaned_data['username']).exists():
                return teacher_list_view(request, 'username')
            teacher_id = Teacher.add({
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email']
            })
            return HttpResponseRedirect(f'/teachers/details/{teacher_id}')
        else:
            return teacher_list_view(request)
    else:
        return teacher_list_view(request)


# /teachers/delete
@login_required
@permission_required('school.delete_teacher', raise_exception=True)
def teacher_delete(request):
    if request.method == 'POST':
        form = DeleteTeacherForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            Teacher.remove(teacher_id)
            return HttpResponseRedirect('/teachers')
        else:
            return teacher_list_view(request)
    else:
        return teacher_list_view(request)


# /teachers/change
@login_required
@permission_required('school.change_teacher', raise_exception=True)
def teacher_change(request):
    if request.method == 'POST':
        form = ChangeTeacherForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            teacher = Teacher.get_by_id(teacher_id)
            if teacher.username != form.cleaned_data['username']:
                if Teacher.objects.filter(username=form.cleaned_data['username']).exists():
                    return teacher_view(request, teacher_id, 'username')
            Teacher.edit({
                'teacher_id': teacher_id,
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email']
            })
            return HttpResponseRedirect(f'/teachers/details/{teacher_id}')
        else:
            return teacher_view(request, form.cleaned_data['teacher_id'])
    else:
        return teacher_list_view(request)


# /parents
@login_required
@permission_required('school.view_parent', raise_exception=True)
def parent_list_view(request, error_message=None):
    # Search
    if request.GET.get('search'):
        parents_list = Parent.find(request.GET.get('search'))
    else:
        parents_list = Parent.get_all()

    # Paginator
    paginator = Paginator(parents_list, 10)
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    parents_page = paginator.get_page(page_number)
    paginator = {
        'actual_page': page_number,
        'has_next': parents_page.has_next(),
        'has_prev': parents_page.has_previous()
    }
    if paginator['has_next']: 
        paginator['next_page'] = parents_page.next_page_number()
    if paginator['has_prev']: 
        paginator['prev_page'] = parents_page.previous_page_number()

    data = {
        'parents': parents_page,
        'paginator': paginator,
        'error': error_message
    }
    return render(request, 'users/parent_list.html', {'data': data})


# /parents/add
@login_required
@permission_required('school.add_parent', raise_exception=True)
def parent_add(request):
    if request.method == 'POST':
        form = AddParentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            if Parent.objects.filter(username=form.cleaned_data['username']).exists():
                return student_view(request, student_id, 'username')
            Parent.add({
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'student_id': student_id
            })
            return HttpResponseRedirect(f'/students/details/{student_id}')
        else:
            return student_list_view(request)
    else:
        return student_list_view(request)


# /parents/delete
@login_required
@permission_required('school.delete_parent', raise_exception=True)
def parent_delete(request):
    if request.method == 'POST':
        form = DeleteParentForm(request.POST)
        if form.is_valid():
            Parent.delete(*[
                Parent.get_by_id(form.cleaned_data['parent_id'])
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /parents/assign
@login_required
@permission_required('school.change_student', raise_exception=True)
def parent_assign(request):
    if request.method == 'POST':
        form = AssignParentForm(request.POST)
        if form.is_valid():
            student = Student.get_by_id(form.cleaned_data['student_id'])
            parent = Parent.get_by_id(form.cleaned_data['parent_id'])
            student.add_parent(parent)            
            return HttpResponseRedirect(f'/students/details/{student.id}')
        else:
            print(form.errors)
            return student_list_view(request)
    else:
        return student_list_view(request)


# /parents/assign/delete
@login_required
@permission_required('school.change_student', raise_exception=True)
def parent_assign_delete(request):
    if request.method == 'POST':
        form = AssignParentForm(request.POST)
        if form.is_valid():
            student = Student.get_by_id(form.cleaned_data['student_id'])
            parent = Parent.get_by_id(form.cleaned_data['parent_id'])
            student.delete_parent(parent)
            return HttpResponseRedirect(form.cleaned_data['next'])
        else:
            print(form.errors)
            return student_list_view(request)
    else:
        return student_list_view(request)


# /parents/details/id
@login_required
@permission_required('school.view_parent', raise_exception=True)
def parent_view(request, id, error_message=None):
    parent = Parent.get_by_id(id)
    data = {
        'parent': parent,
        'students': parent.get_students(),
        'error': error_message
    }
    return render(request, 'users/parent.html', {'data': data})


# /parents/change
@login_required
@permission_required('school.change_parent', raise_exception=True)
def parent_change(request):
    if request.method == 'POST':
        form = ChangeParentForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data['parent_id']
            parent = Parent.get_by_id(parent_id)
            if parent.username != form.cleaned_data['username']:
                if Parent.objects.filter(username=form.cleaned_data['username']).exists():
                    return parent_view(request, parent_id, 'username')
            Parent.edit({
                'parent_id': parent_id,
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email']
            })
            return HttpResponseRedirect(f'/parents/details/{parent_id}')
        else:
            return student_view(request, form.cleaned_data['parent_id'])
    else:
        return student_list_view(request)


# /timetables
@login_required
def time_table_list_view(request):
    if request.user.groups.filter(name="Principals").exists():
        # Show all classes
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'time_tables/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Teachers").exists():
        # Show all classes
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'time_tables/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Parents").exists():
        # Show only kids classes
        parent = Parent.get_by_id(request.user.id)
        students = parent.get_students()
        available_classes = [student.student.get_class() for student in students]
        data = {
            'classes': available_classes
        }
        return render(request, 'time_tables/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Students").exists():
        # Show only student class
        student = Student.get_by_id(request.user.id)
        squad = student.get_class()
        return time_table_view(request, squad.id)
    else:
        # Show all classes
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'time_tables/class_list.html', {'data': data})


# /timetables/details/id
@login_required
def time_table_view(request, id):
    requested_class = Squad.get_by_id(id)
    time_tables = TimeTable.get_by_class(requested_class)
    subjects = requested_class.get_subjects()
    data = {
        'squad': requested_class,
        'time_tables': time_tables,
        'subjects': subjects
    }
    return render(request, 'time_tables/timetable.html', {'data': data})


# /timetables/add
@login_required
@permission_required('school.change_timetable', raise_exception=True)
def time_table_add(request):
    if request.method == 'POST':
        form = AddLessonForm(request.POST)
        if form.is_valid():
            squad = Squad.get_by_id(form.cleaned_data['squad_id'])
            squad.add_lesson(*[
                form.cleaned_data['day'],
                LessonTable.get_by_id(form.cleaned_data['lesson_id']),                
                SquadSubject.get_by_id(form.cleaned_data['subject_id'])
            ])
            return HttpResponseRedirect(f'/timetables/details/{ squad.id }')
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /timetables/delete
@login_required
@permission_required('school.change_timetable', raise_exception=True)
def time_table_delete(request):
    if request.method == 'POST':
        form = DeleteLessonForm(request.POST)
        if form.is_valid():
            squad = Squad.get_by_id(form.cleaned_data['squad_id'])
            squad.delete_lesson(*[
                form.cleaned_data['time_table_id']
            ])
            return HttpResponseRedirect(f'/timetables/details/{ squad.id }')
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /timetables/change
@login_required
@permission_required('school.change_timetable', raise_exception=True)
def time_table_change(request):
    if request.method == 'POST':
        form = ChangeLessonForm(request.POST)
        if form.is_valid():
            squad = Squad.get_by_id(form.cleaned_data['squad_id'])
            squad.change_lesson(*[
                form.cleaned_data['time_table_id'],
                form.cleaned_data['subject_id']
            ])
            return HttpResponseRedirect(f'/timetables/details/{ squad.id }')
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /grades
@login_required
def grade_list_view(request):
    if request.user.groups.filter(name="Principals").exists():
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'grades/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Teachers").exists():
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'grades/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Parents").exists():
        parent = Parent.get_by_id(request.user.id)
        students = parent.get_students()
        students = [student.student for student in students]
        data = {
            'students': students
        }
        print(data)
        return render(request, 'grades/student_list.html', {'data': data})
    elif request.user.groups.filter(name="Students").exists():
        student = Student.get_by_id(request.user.id)
        return grade_view(request, student.id)
    else:
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'grades/class_list.html', {'data': data})


# /grades/class/id
@login_required
@permission_required('school.view_grade', raise_exception=True)
def grade_class_view(request, id):
    squad = Squad.get_by_id(id)
    data = {
        'students': squad.get_all_students()
    }
    return render(request, 'grades/student_list.html', {'data': data})


# /grades/student/id
@login_required
@permission_required('school.view_grade', raise_exception=True)
def grade_view(request, id):
    student = Student.get_by_id(id)
    data = {
        'student': student,
        'grades': student.get_grades()
    }
    return render(request, 'grades/grades.html', {'data': data})


# /grades/add
@login_required
@permission_required('school.add_grade', raise_exception=True)
def grade_add(request):
    if request.method == 'POST':
        form = AddGradeForm(request.POST)
        if form.is_valid():
            student = Student.get_by_id(form.cleaned_data['student_id'])
            student.add_grade(*[
                request.user,
                SquadSubject.get_by_id(form.cleaned_data['subject_id']),
                form.cleaned_data['grade'],
                form.cleaned_data['description']
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /grades/change
@login_required
@permission_required('school.change_grade', raise_exception=True)
def grade_change(request):
    if request.method == 'POST':
        form = ChangeGradeForm(request.POST)
        if form.is_valid():
            grade = Grade.get_by_id(form.cleaned_data['grade_id'])
            grade.change(*[
                request.user,
                form.cleaned_data['grade'],
                form.cleaned_data['description']
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /grades/delete
@login_required
@permission_required('school.delete_grade', raise_exception=True)
def grade_delete(request):
    if request.method == 'POST':
        form = DeleteGradeForm(request.POST)
        if form.is_valid():
            grade = Grade.get_by_id(form.cleaned_data['grade_id'])
            grade.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /attendance
@login_required
def attendance_list_view(request):
    if request.user.groups.filter(name="Principals").exists():
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'attendance/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Teachers").exists():
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'attendance/class_list.html', {'data': data})
    elif request.user.groups.filter(name="Parents").exists():
        parent = Parent.get_by_id(request.user.id)
        students = parent.get_students()
        students = [student.student for student in students]
        data = {
            'students': students
        }
        return render(request, 'attendance/student_list.html', {'data': data})
    elif request.user.groups.filter(name="Students").exists():
        student = Student.get_by_id(request.user.id)
        return attendance_view(request, student.id)
    else:
        data = {
            'classes': Squad.get_all()
        }
        return render(request, 'attendance/class_list.html', {'data': data})


# /attendance/class/id
@login_required
@permission_required('school.view_attendance', raise_exception=True)
def attendance_class_view(request, id):
    squad = Squad.get_by_id(id)
    data = {
        'students': squad.get_all_students()
    }
    return render(request, 'attendance/student_list.html', {'data': data})


# /attendance/student/id
@login_required
@permission_required('school.view_attendance', raise_exception=True)
def attendance_view(request, id):
    student = Student.get_by_id(id)
    data = {
        'student': student,
        'lessons': LessonTable.get_all(),
        'event_types': Attendance.get_event_types(),
        'attendances': student.get_attendance()
    }
    return render(request, 'attendance/attendances.html', {'data': data})


# /attendance/add
@login_required
@permission_required('school.add_attendance', raise_exception=True)
def attendance_add(request):
    if request.method == 'POST':
        form = AddAttendanceForm(request.POST)
        if form.is_valid():
            student = Student.get_by_id(form.cleaned_data['student_id'])
            student.add_attendance(*[
                request.user,
                LessonTable.get_by_id(form.cleaned_data['lesson_id']),
                form.cleaned_data['event'],
                form.cleaned_data['date']
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /attendance/change
@login_required
@permission_required('school.change_attendance', raise_exception=True)
def attendance_change(request):
    if request.method == 'POST':
        form = ChangeAttendanceForm(request.POST)
        if form.is_valid():
            attendance = Attendance.get_by_id(form.cleaned_data['attendance_id'])
            attendance.change(*[
                request.user,
                LessonTable.get_by_id(form.cleaned_data['lesson_id']),
                form.cleaned_data['event'],
                form.cleaned_data['date']
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /attendance/delete
@login_required
@permission_required('school.delete_attendance', raise_exception=True)
def attendance_delete(request):
    if request.method == 'POST':
        form = DeleteAttendanceForm(request.POST)
        if form.is_valid():
            attendance = Attendance.get_by_id(form.cleaned_data['attendance_id'])
            attendance.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# /message/list
@login_required
# @permission_required('school.view_message', raise_exception=True)
def message_list_view(request):
    user = MyUser.get_by_id(request.user.id)
    data = {
        'user': request.user,
        'messages': user.get_all_messages_list(),
        'principals': Principal.get_all(),
        'teachers': Teacher.get_all(),
        'parents': Parent.get_all(),
        'students': Student.get_all()
    }
    return render(request, 'messages/messages_list.html', {'data': data})


# /messages
@login_required
# @permission_required('school.view_message', raise_exception=True)
def messages_view(request):
    data = {
        
    }
    return render(request, 'messages/messages.html', {'data': data})


# /message/send
@login_required
# @permission_required('school.add_message', raise_exception=True)
def message_send(request):
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender = MyUser.get_by_id(form.cleaned_data['sender_id'])
            recipient = MyUser.get_by_id(form.cleaned_data['recipient_id'])
            Message.send(*[
                sender,
                recipient,
                form.cleaned_data['message']
            ])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))