from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from . import models
from .models import Paciente
from .forms import SignUpForm


# Create your views here.

def index(request):
    return render(request, 'index.html')

def usuarios(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'appGestionHospitalaria/index.html', context)
    #return render(request, 'appGestionHospitalaria/index.html')
    return HttpResponse("Hello, world. You're at the users index.")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Inicio')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

