from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import *
from .models import LessonTable, Squad, ClassProfile, Student, Parent, Subject, TimeTable


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
def student_list_view(request):
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
        'paginator': paginator
    }
    return render(request, 'users/student_list.html', {'data': data})


# /students/details/id
@login_required
@permission_required('school.view_student', raise_exception=True)
def student_view(request, id):
    student = Student.get_by_id(id)
    data = {
        'student': student,
        'parents': student.get_parents(),
        'classes': Squad.get_all(),
        'parents_list': Parent.get_all()
    }
    return render(request, 'users/student.html', {'data': data})


# /students/add
@login_required
@permission_required('school.add_student', raise_exception=True)
def student_add(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
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
@permission_required('school.delete_classprofile', raise_exception=True)
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


# /parents
@login_required
@permission_required('school.view_parent', raise_exception=True)
def parent_list_view(request):
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
        'paginator': paginator
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
def parent_view(request, id):
    parent = Parent.get_by_id(id)
    data = {
        'parent': parent,
        'students': parent.get_students()
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


# /timetables/details/id
@login_required
def time_table_view(request, id):
    requested_class = Squad.get_by_id(id)
    time_tables = TimeTable.get_by_class(requested_class)
    data = {
        'time_tables': time_tables
    }
    return render(request, 'time_tables/timetable.html', {'data': data})
