from django.shortcuts import render
from .forms import LoginForm, SignupForm


def home(request):
	return render(request, "base.html", 
						{
							'page': 'pages/home.html',
							'active_nav': 'home',
			})

def login(request):
	return render(request, 'base.html',
					{
						'page': 'pages/login.html',
						'active_nav': 'login',
						'form': LoginForm(),
					})

def signup(request):
	return render(request, 'base.html',
					{ 
						'page': 'pages/signup.html',
						'active_nav': 'signup',
						'form': SignupForm(),
					})