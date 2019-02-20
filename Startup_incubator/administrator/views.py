from django.shortcuts import render

from .models import Incubation,Fund,Updates,Documents,Milestones,Reviews

from .models import Incubation,Fund,Updates,Documents
from django.shortcuts import render
from startup.models import Startup,Founder,Tickets
from login.models import Type
from investor.models import Investor
from mentor.models import Mentor
from django.contrib.auth.models import User
from investor.models import Investor
from mentor.models import Mentor
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime
from administrator.models import AssignMentor

# just a helper function. it can be reused for getting admin names
def get_admin(id):
 	admin = User.objects.get(id=id)
 	return admin


def dashboard(request):
	if not request.user.is_authenticated() :
		print("Not authenticated")
	msg = ""
	if request.session.get('message', False):
		msg = request.session.get('message')
		del request.session['message']
		print(msg)
	return render(request,'administrator/dashboard.html',{'admin':get_admin(request.user.id),'msg':msg})




@csrf_exempt
#for admin to add mentor
def add_mentor(request):
	if not request.user.is_authenticated() :
		return redirect('/login')


	if request.method =='GET':
		return render(request,'administrator/addmentor.html',{'admin':get_admin(request.user.id)})
	else:
		name = request.POST.get('name')
		print(name)

		email = request.POST.get('email')
		password = request.POST.get('password')	
		
		
		print(password)
		user = User()
		user.username = name
		user.set_password(password)
		user.email = email
		user.is_active = True
		user.save()
		typ = Type()
		typ.user_id = user.id
		typ.typ = "mentor"
		typ.save()
		mentor = Mentor()
		mentor.user_id = typ.id
		mentor.name = name
		mentor.email = email
		#mentor.password = password
		mentor.save()
		mail_subject = 'Your account has been activated'
		message = 'Hi ' +  str(name) + 'your account has been activated.Your username is '+ str(email) + ' password is  ' +str(password) 
		to_email = email
		email1 = EmailMessage(mail_subject, message, to=[to_email])
		email1.send()
		request.session['message'] = "Mentor successfully added !"
		return redirect('/administrator')


@csrf_exempt		
def add_investor(request):

	if request.method =='GET':
		return render(request,'administrator/addinvestor.html',{'admin':get_admin(request.user.id)})
	else:
		name = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = User()
		user.username = name
		user.set_password(password)
		user.email = email
		user.is_active = True
		user.save()
		typ = Type()
		typ.user_id = user.id
		typ.typ = "investor"
		typ.save()
		investor = Investor()
		investor.user_id = typ.id
		investor.name = name
		#investor.password = password
		investor.email = email
		investor.save()
		mail_subject = 'Your account has been activated'
		message = 'Hi ' +  str(name) + 'your account has been activated.Your username is '+ str(email) + ' password is  ' +str(password) 
		to_email = email
		email1 = EmailMessage(mail_subject, message, to=[to_email])
		email1.send()
		request.session['message'] = "Investor successfully added !"
		return redirect('/administrator')




#show profiles
def show_startups(request):
	if not request.user.is_authenticated() :
		return redirect('/login')
	
	startups = Startup.objects.all()
	size = len(startups)
	left = int(size/2)

	startups_right = startups[:left]
	startups_left = startups[left:]

	return render(request, 'administrator/showstartups.html',{'startups_left':startups_left,
															  'startups_right':startups_right,
															  	'admin':get_admin(request.user.id)})


def show_investors(request):
	if not request.user.is_authenticated() :
		return redirect('/login')


	investors = Investor.objects.all()
	size = len(investors)
	left = int(size/2)

	investors_right = investors[:left]
	investors_left = investors[left:]
	return render(request, 'administrator/showinvestor.html',{'investors_left':investors_left,
															  'investors_right':investors_right,
												              'admin':get_admin(request.user.id)})


def show_mentors(request):
	if not request.user.is_authenticated() :
		return redirect('/login')
	mentors = Mentor.objects.all()
	size = len(mentors)
	left = int(size/2)

	mentors_right = mentors[:left]
	mentors_left = mentors[left:]
	startup = Startup.objects.get(user__user_id=request.user.id)
	return render(request, 'administrator/showmentors.html',{'mentors_left':mentors_left,
															  'mentors_right':mentors_right,
															  'admin':get_admin(request.user.id)})



@csrf_exempt
def upload_documents(request):
	startups = Startup.objects.all()

	documents = Documents.objects.all()
	
	if request.method =="GET":
		docs = []
		for s in startups:
			docs_of_s = Documents.objects.filter(startup_id=s.id,typ='admin')
			for d in docs_of_s:
				docs.append(d.doc.url)
		print(docs)

		return render(request, 'administrator/uploaddocs.html',{'errormessage':'',
																'admin':get_admin(request.user.id),
																'documents':docs})
	else:
		doc = request.FILES.get('file',False)
		for startup in startups:
			document = Documents()
			document.doc = doc
			document.startup_id = startup.id
			document.typ = 'admin'
			document.save()
		request.session["message"] = "Document uploaded successfully"
		return redirect('/administrator')

@csrf_exempt
#posts updates in main page
def update_info(request):
	if not request.user.is_authenticated() :
		return redirect('/login')

	if request.method == "GET":
		return render(request, 'administrator/addupdates.html',{'admin':get_admin(request.user.id)})
	
	else:
		info = request.POST['about']
		schedule = request.POST['schedule']
		title = request.POST['title']
		updates = Updates()
		updates.info = info
		updates.schedule =schedule
		updates.title = title
		updates.image = request.FILES.get('image',False)
		print(updates.image)
		updates.save()
		print(updates.date)
		print(updates.schedule)
		return render(request,'administrator/addupdates.html',{'errormessage':'success','admin':get_admin(request.user.id)})


def show_incubation(request):
	if not request.user.is_authenticated() :
		return redirect('/login')
	msg = ""
	if request.session.get('message', False):
		msg = request.session.get('message')
		del request.session['message']
	incubation = Incubation.objects.filter(clicked=False)
	print(len(incubation))
	return render(request, 'administrator/incubation_evaluation.html',{'msg':msg,
																		'incubation':incubation,
																		'admin':get_admin(request.user.id)})



def show_fund(request):
	if not request.user.is_authenticated() :
		return redirect('/login')
	msg = ""
	if request.session.get('message', False):
		msg = request.session.get('message')
		del request.session['message']
		
	fund = Fund.objects.filter(clicked=False)
	return render(request, 'administrator/showfund.html',{'fund':fund,'admin':get_admin(request.user.id)})

def accept_incubation(request,pk):
	incubation = Incubation.objects.get(startup_id=pk)
	incubation.clicked = True
	incubation.accept = True
	incubation.save()
	request.session['message'] = str(incubation.startup.name) + " incubation request ACCEPTED !" 
	return redirect("/administrator/show_incubation")

def reject_incubation(request,pk):
	#response = request.POST['response']
	incubation = Incubation.objects.get(startup_id=pk)
	incubation.clicked = True
	incubation.save()
	request.session['message'] = str(incubation.startup.name) + "'s incubation request REJECTED !"
	return redirect("/administrator/show_incubation")


def accept_fund(request,pk):
	#response = request.POST['response']
	fund = Fund.objects.get(startup_id=pk)
	fund.clicked = True
	fund.accept = True
	fund.save()
	return redirect("/administrator/show_fund")

def reject_fund(request,pk):
	#response = request.POST['response']
	fund = Fund.objects.get(startup_id=pk)
	fund.clicked = True
	fund.save()
	return redirect("/administrator/show_fund")

def show_tickets(request):

	tickets = Tickets.objects.filter(status=False)
	left = int(len(tickets)/2)
	left_tickets = tickets[left:]
	right_tickets = tickets[:left]
	return render(request,'administrator/showtickets.html',{'admin':get_admin(request.user.id),'left_tickets':left_tickets,'right_tickets':right_tickets,'msg':''})


def show_ticket(request,pk):
	ticket = Tickets.objects.get(id=pk)
	return render(request,'administrator/ticketdetails.html',{'admin':get_admin(request.user.id),'ticket':ticket})


def solve_ticket(request,pk):
	ticket = Tickets.objects.get(id=pk)
	ticket.solved_date = datetime.datetime.now()
	ticket.status = True
	ticket.save()
	return render(request,'administrator/showtickets.html',{'admin':get_admin(request.user.id),'ticket':ticket,'msg':'done'})


def assign_mentor(request):

	return render(request,'administrator/assignmentor.html',{})



@csrf_exempt
def assign_mentor(request):
	if request.method == "GET":

		mentors = Mentor.objects.all()
		startups = Startup.objects.all()
		size = len(mentors)
		left = int(size/2)

		mentors_right = mentors[:left]
		mentors_left = mentors[left:]
		print(len(mentors_right),len(mentors_left))
		return render(request,'administrator/assignmentor.html',{'admin':get_admin(request.user.id),
																 'startups':startups,
																 'mentors_left':mentors_left,
																 'mentors_right':mentors_right})
	else:

		name = request.POST.get("startup")
		
		startup = Startup.objects.get(name=name)
		
		assign = AssignMentor()
		assign.months = request.POST.get('months')
		assign.startup_id = startup.id

		mentor = Mentor.objects.get(id=request.POST.get('id'))
		assign.mentor_id = mentor.id
		assign.save()
		request.session['message'] = "Assigned the mentor"
		return redirect('/administrator')

		return render(request,'front/login.html')


@csrf_exempt
def set_milestone(request,pk):
	if request.method == "GET":
		startup = Startup.objects.get(id=pk)
		return render(request,'administrator/setmilestone.html',{'admin':get_admin(request.user.id),'startup':startup})
	else:
		startup = Startup.objects.get(id=pk)
		milestone = Milestones()
		milestone.title = request.POST['title']
		date = request.POST['deadline']
		milestone.description = request.POST['description']
		val = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
		milestone.deadline = datetime.datetime.strptime(val, "%Y-%m-%d").date()
		milestone.startup_id = pk
		milestone.save()
		
		startups = Startup.objects.filter(admin_funded=True)
		size = len(startups)
		left = int(size/2)
		startups_right = startups[:left]
		startups_left = startups[left:]
		return render(request, 'administrator/showfundedstartups.html',{'startups_left':startups_left,
															  'startups_right':startups_right,
	
															  	'admin':get_admin(request.user.id),'msg':'success'})

def show_milestone(request,pk):
	startup = Startup.objects.get(id=pk)
	milestones = Milestones.objects.filter(startup_id=startup.id)
	return render(request,'administrator/timeline.html',{'admin':get_admin(request.user.id),'milestones':milestones})

def show_funded_startups(request):
	if not request.user.is_authenticated() :
		return redirect('/login')
	
	startups = Startup.objects.filter(admin_funded=True)
	size = len(startups)
	left = int(size/2)

	startups_right = startups[:left]
	startups_left = startups[left:]

	return render(request, 'administrator/showfundedstartups.html',{'startups_left':startups_left,
															  'startups_right':startups_right,
															  	'admin':get_admin(request.user.id),'msg':''})

def complete_milestone(request,pk):
	print("tets")
	milestone = Milestones.objects.get(id=pk)
	milestone.completed_admin  = 1
	
	milestone.save()
	
	return redirect("/administrator/show_funded_startups")
def reviews(request):
	reviews = Reviews.objects.all()
	return render(request,'administrator/reviews.html',{'reviews':reviews})

