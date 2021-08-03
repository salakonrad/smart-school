from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm
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
def class_list_view(request):
    data = {
        'classes': Squad.objects.all()
    }
    return render(request, 'class/class_list.html', {'data': data})