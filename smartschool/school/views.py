from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, AddSquadForm, DeleteSquadForm
from .models import Squad


def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    return render(request, 'auth/login.html')

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

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

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

@login_required
@permission_required('school.add_squad', raise_exception=True)
def class_add(request):
    if request.method == 'POST':
        form = AddSquadForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            class_profile = form.cleaned_data['profile']
            class_supervisor = form.cleaned_data['supervisor']
            Squad.add({
                'name': class_name,
                'profile': class_profile,
                'supervisor': class_supervisor
            }, request.user)
            return HttpResponseRedirect('/classes')
        else:
            return class_list_view(request, form.errors)
    else:
        return class_list_view(request)

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