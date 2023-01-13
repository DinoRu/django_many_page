from .forms import LoginForm, SignupForm
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

def send_page(self, page):

	"""Render HTML and send page to client"""
	# Prepare the context for the page
	context = {}
	match page:
		case 'home':
			context = {
				"tasks": self.scope["session"]["tasks"] if "tasks" in self.scope["session"] else []
			}

		case 'login':
			context = {
				'form': LoginForm()
			}

		case 'signup':
			context={'form': SignupForm()}

	context.update({'active_nav': page})

	# Render HTML nav and send to the client
	self.send_html({
			'selector': '#nav',
			'html': render_to_string('components/_nav.html', context)
		})

	# Render HTML page and send to the client
	self.send_html({
			'selector': '#main',
			'html': render_to_string(f"pages/{page}.html", context),
			'url': reverse(page)
		})

def action_signup(self, data):
	""" Sign up user """
	form = SignupForm(data)
	user_exist = User.objects.filter(email=data['email']).exists()
	if form.is_valid() and data['password'] == data['password_confirm'] and not user_exist:
		# Create user
		user = User.objects.create_user(data["username"], email=data["email"], password=data["password"])
		user.is_active = True
		user.save()
		# Login user
		send_page(self, "login")
	else:
		# Send form errors
		self.send_html({
			"selector": "#main",
			"html": render_to_string("pages/signup.html", {"form": form, "user_exist": user_exist, "password_do_not_match": data["password"] != data["password_confirm"]}),
			"append": False,
			"url": reverse("signup")
			})


def add_lap(self):
	self.send_html({
			'selector': '#laps',
			'html': render_to_string('components/_lap.html', {"time": datetime.now()}),
			'append': True,
		})

def add_task(self, data):
	self.send_html({
			"selector": "#todo",
			"html": render_to_string("components/_task-item.html", {"task": data["task"]}),
			"append": True
		})
	# Make 
	self.scope["session"]["tasks"].append(data["task"])
	self.scope["session"].save()