from django.shortcuts import render,redirect
from django.http import HttpResponse
from investor.models import Investor, Connections
from recommendations.train import train_model
from recommendations.test import predict
import operator
from .models import Startup,Tickets,Bookings

from .models import Startup
from administrator.models import Fund,Incubation,AssignMentor,Documents,Milestones

from .models import Startup,Tickets

from administrator.models import Fund,Incubation,Reviews
from rent.models import Rent
from mentor.models import Mentor
from django.views.decorators.csrf import csrf_exempt
from datetime import date,datetime
from login.models import Type

import calendar
from django.utils.dateparse import parse_date

def dashboard(request):
	if request.user.is_authenticated() :
		startup = Startup.objects.get(user__user_id=request.user.id)
		try :
			startup = Startup.objects.get(user__user_id=request.user.id)
		except:
			print("wrong")

		msg = ""
		if request.session.get('message', False):
			msg = request.session.get('message')
			del request.session['message']
			print(msg)
		incubation_request = Incubation.objects.filter(startup__user__user_id=request.user.id)
		accepted = "false"
		if len(incubation_request) > 0:
			if incubation_request[0].accept :
				accepted ="true"

		
		investors = []
		recommend = {"email":"none","name":"none"}
		if len(Investor.objects.all()) < 2:
			return render(request,"startup/dashboard.html",{'startup':startup,'msg':msg,'accepted':accepted,
														'recommend':recommend})
		for i in Investor.objects.all():
			temp = [i.name,i.description]
			investors.append(temp)
		print("before predict")
		result = predict(investors,startup.description)

		result = sorted(result, key=operator.itemgetter(1))
		result = result[::-1]

		print("result",result)
		recommend = Investor.objects.all()[0]
		investor = Investor.objects.filter(name=result[0][1])
		if len(investor) > 0:
			recommend = investor[0]
		
		return render(request,"startup/dashboard.html",{'startup':startup,'msg':msg,'accepted':accepted,
														'recommend':recommend})
	else:
		return redirect('/login')
	


def get_recommendations(request):
	if not request.user.is_authenticated() :
		return redirect('/login')

	startup = "trucks vehicle"
	investors = Investor.objects.all()
	data = []
	for i in investors:
		obj = []
		obj.append(i.name)
		obj.append(i.description)
		data.append(obj)
	predict(data,startup)
	return HttpResponse("done")

def train(request):
	print("Training the model ..... wait.....")

	train_model()

	return HttpResponse('trained successfully !')


def test(request):
	
	investors = []
	for i in Investor.objects.all():
		temp = [i.name,i.description]
		investors.append(temp)
	print("Investor ", investors)
	startup = "my startup gives tech solutions to other startups"
	# startup = "my deals cool bikes  with startup provides software development Site machine learning and cloud docker systems."
	# investors = [['jain_softwares'," Software Development "],
	# 			['bikes',"my startup deals with cool bikes."]
	# 			]
				
	return predict(investors,startup)



def about_us(request):
	if request.user.is_authenticated() :
		startup = Startup.objects.get(user__user_id=request.user.id)
		print(startup.name)
		return render(request,"startup/about.html",{'startup':startup,'accepted':"true"})
	else:
		return render(request,'front/login.html')
	
def mentors(request):
	if request.user.is_authenticated() :
		mentors = []
		assigns = AssignMentor.objects.filter(startup__user__user_id=request.user.id)
		for a in assigns:
			temp = {}
			temp["name"] = a.mentor.name
			temp["months"] = a.months
			temp["date"] = a.date
			temp["description"] = a.mentor.description
			temp["id"] = a.mentor.id
			temp["image"] = a.mentor.image.url
			mentors.append(temp)
		size = len(mentors)
		left = int(size/2)
		mentors_right = mentors[:left]
		mentors_left = mentors[left:]

		startup = Startup.objects.get(user__user_id=request.user.id)
		return render(request,"startup/mentor.html",{'mentors_left':mentors_left,
													'mentors_right':mentors_right,
													'startup':startup,
													'accepted':"true"})
	else:
		return render(request,'front/login.html')


def startup_profile_popup(request,pk):
	startup = Startup.objects.get(id=pk)
	return render(request,'startup/startup_profile_popup.html',{'startup':startup,'accepted':"true"})

def mentor_profile_popup(request,pk):
	mentor = Mentor.objects.get(id=pk)
	return render(request,'startup/mentor_profile_popup.html',{'mentor':mentor,'accepted':"true"})

def investors(request):
	if request.user.is_authenticated() :

		investors = Investor.objects.all()
		investor_data = []
		for m in investors:
			temp = {}
			temp["investor_user_id"] = m.user.user.id
			temp["id"] = m.id
			temp["name"] = m.name
			temp["image"] = m.image.url
			temp["description"] = m.description

			obj = Connections.objects.filter(sentfrom_id=request.user.id,sentto_id=m.user.user.id)
			if( len(obj) >= 1 ):
				obj = obj[0]
				if obj.accept == True:
					temp["pending"] = 2
				elif obj.response == True:
					temp["pending"] = 1
				else:
					temp["pending"] = 1
			else:
				temp["pending"] = 0
			investor_data.append(temp)

		print(investor_data)
		size = len(investor_data)
		left = int(size/2)

		investors_right = investor_data[:left]
		investors_left = investor_data[left:]
		startup = Startup.objects.get(user__user_id=request.user.id)
		return render(request,"startup/investor.html",{'investors_left':investors_left,
													'investors_right':investors_right,
													'startup':startup,
													'accepted':"true"})
	else:
		return render(request,'front/login.html')

def investor_profile_popup(request,pk):
	investor = Investor.objects.get(id=pk)
	return render(request,'startup/investor_profile_popup.html',{'investor':investor,'accepted':"true"})

@csrf_exempt
def apply_incubation(request):
	if request.user.is_authenticated() :
		print('authenticated')

	if request.method == 'GET':
		try:
			startup = Startup.objects.get(user__user_id=request.user.id)
		except:
			return HttpResponse("User does not have a startup")

		return render(request,'startup/apply_incubation.html',{'startup':startup,"accepted":"false"})
	else:
		try:
			startup = Startup.objects.get(user__user_id=request.user.id)
		except:
			return HttpResponse('No startups of this user')

		requests = Incubation.objects.filter(startup__user__user_id=request.user.id)
		fg = 0
		for req in requests:
			if req.clicked == False:
				fg = 1
				break
		if fg == 1:
			request.session['message'] = "You have already applied for Incubation. Wait for reply"
			return redirect('/startup')

		incubation_request = Incubation()
		incubation_request.startup_id = startup.id
		incubation_request.ppt = request.FILES.get('ppt',False)
		incubation_request.save()
		if incubation_request.ppt is False :
			request.session['message'] = "Could not save presentation !" 
		else:
			request.session['message'] = "Applied for Incubation successfully !"
		return redirect('/startup')



@csrf_exempt
def apply_fund(request):
	if request.method == 'GET':
		try:
			startup = Startup.objects.get(user__user_id=request.user.id)
		except:
			return HttpResponse("User does not have a startup")

		return render(request,'startup/apply_fund.html',{'startup':startup,'accepted':"true"})
	else:
		try:
			startup = Startup.objects.get(user__user_id=request.user.id)
		except:
			return HttpResponse('No startups of this user')

		requests = Fund.objects.filter(startup__user__user_id=request.user.id)
		fg = 0
		for req in requests:
			if req.clicked == False:
				fg = 1
				break
		if fg == 1:
			request.session['message'] = "You have already applied for Fund. Wait for reply"
			return redirect('/startup')

		fund_request = Fund()
		fund_request.startup_id = startup.id
		fund_request.typ = request.POST['type']
		fund_request.ppt = request.FILES.get('ppt',False)
		fund_request.save()
		if fund_request.ppt is False :
			request.session['message'] = "Could not save presentation !" 
		else:
			request.session['message'] = "Applied for Fund successfully !"
		return redirect('/startup')
	


def send_connection_request(request,pk):
	# from will be the logged in user
	fromm = Type.objects.get(user_id=request.user.id)
	# to will be sent from connect button
	to = Type.objects.get(user_id=pk)
	connections = Connections()
	connections.sentfrom_id = fromm.user.id
	connections.sentto_id = pk
	connections.save()
	request.session['message'] = "Sent Connection request "
	return redirect('/startup/')


def show_connections(request):
	connections1 = Connections.objects.filter(sentfrom_id=request.user.id,accept=True)
	print(len(connections1))
	connections2 = Connections.objects.filter(sentto_id=request.user.id,accept=True)
	print(len(connections1))
	startups = []
	for connection in connections1:
		sentto = connection.sentto
		typ = Type.objects.get(user_id=sentto.id)
		if typ.typ == "investor":
			print("got1")
			name = Investor.objects.get(user_id=typ.id)
			print(name.description)
			startups.append(name)
	for connection in connections2:
		sentfrom = connection.sentfrom
		typ = Type.objects.get(user_id=sentfrom.id)
		if typ.typ == "investor":
			name = Investor.objects.get(user_id=typ.id)
			print("got1")
			startups.append(name)
	print(startups)
	x = []
	for s in startups:
		obj = {}
		obj["name"] = s.name
		obj["id"] = s.id
		obj["image"] = s.image.url
		print(obj["image"])
		obj["description"] = s.description
		x.append(obj)
	left = int(len(x)/2)
	print(left)
	startups_left = x[:left]
	startups_right = x[left:]
	startup = Startup.objects.get(user__user_id=request.user.id)
	return render(request, 'startup/myconnections.html',{'startup':startup,
														 'startups_left':startups_left,
														 'startups_right':startups_right,
														 'accepted':"true"})


def show_pending_connections(request):
	connections2 = Connections.objects.filter(sentto_id=request.user.id,response=False)
	
	startups = []
	for connection in connections2:
		sentfrom = connection.sentfrom
		typ = Type.objects.get(user_id=sentfrom.id)
		if typ.typ == "investor":
			name = Investor.objects.get(user_id=typ.id)
			print("got1")
			startups.append(name)
	print(startups)
	x = []
	for s in startups:
		obj = {}
		obj["name"] = s.name
		obj["id"] = s.id
		obj["image"] = s.image.url
		print(obj["image"])
		obj["description"] = s.description
		x.append(obj)
	left = int(len(x)/2)
	print(left)
	startups_left = x[:left]
	startups_right = x[left:]
	startup = Startup.objects.get(user__user_id=request.user.id)
	return render(request, 'startup/mypendingconnections.html',{'startup':startup,
																'startups_left':startups_left,
																'startups_right':startups_right,
																'accepted':"true"})

def accept_connection(request,pk):
	print("das")
	startup = Startup.objects.get(user__user_id=request.user.id)
	try:
		investor = Investor.objects.get(id=pk)
		num = investor.user.user.id
		connection = Connections.objects.get(sentto_id=request.user.id,sentfrom_id=num) 
	except:
		return HttpResponse("error")
	connection.response = True
	connection.accept = True
	connection.save()
	return redirect("/startup/show_pending_connections")

def reject_connection(request,pk):
	startup = Startup.objects.get(user__user_id=request.user.id)

	print("\n",pk)
	investor = Investor.objects.get(id=pk)
	num = investor.user.user.id
	print(num)
	connection = Connections.objects.get(sentto_id=request.user.id,sentfrom_id=num) 
	connection.response = True
	connection.accept = False
	connection.save()
	return redirect("/startup/show_pending_connections")


def my_videos(request):
	startup = Startup.objects.get(user__user_id=request.user.id)
	videos = Documents.objects.filter(startup__user__user_id=request.user.id,category="video")
	if len(videos) == 0:
		request.session["message"] = "No videos yet !"
		return redirect('/startup')
	return render(request,'startup/videolist.html',{'videos':videos,
													'startup':startup,
													'accepted':"true"})

@csrf_exempt
def generate_ticket(request):
	startup = Startup.objects.get(user__user_id=request.user.id)
	if request.method == "GET":
		return render(request,'startup/createtickets.html',{'startup':startup,'msg':'','accepted':"true"})
	else:
		ticket = Tickets()
		ticket.title = request.POST['title']
		ticket.issue = request.POST['issue']
		ticket.startup=startup
		ticket.save()
		return render(request,'startup/createtickets.html',{'startup':startup,
															'msg':'sent',
															'accepted':"true"})

@csrf_exempt
def show_bookings(request):
	if request.method == "GET":
		startup = Startup.objects.get(user__user_id=request.user.id)
		today = date.today()
		print(today)
		bookings = Bookings.objects.filter(date__gt=today).order_by('date')
		store = datetime.today().weekday()
		print("sd")
		for p in bookings:
			p.day = calendar.day_name[p.date.weekday()]
			p.save()

		x = []
		days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
		for i in range(7):
			obj = {}
			obj["day"] = days[i]
			try:
				print("df1")
				book = Bookings.objects.filter(date__gt=today,day=days[i])
				for j in range(10,18):
					try:
						val = Bookings.objects.get(date__gt=today,day=days[i],time=j)
						obj["name"] = val.startup.name
						obj[j] = 1
					except:
						obj[j] = 0
			except:
				print("dfs")
				for j in range(10,18):
					obj[j] = 0
			x.append(obj)
		print(x)
		run = []
		for i in range(10,18):
			run.append(i)
		x_left = x[store:]
		x_right = x[:store]
		x = x_left+x_right
		return render(request,'startup/booking.html',{'bookings':x,
													  'startup':startup,
													  'run':run,
													  'store':store,
													  'accepted':"true"})

@csrf_exempt
def select_booking(request):
	print(request.POST)
	row = request.POST.get('row')
	col = request.POST.get('col')
	a = request.POST.get('today')
	date = datetime.strptime(a, '%Y%m%d').strftime('%Y/%m/%d')
	val = datetime.strptime(date, "%Y/%m/%d").date()
	
	print(type(val))
	booking = Bookings()
	sta = Startup.objects.get(user__user__id=request.user.id)
	booking.startup_id = sta.id
	booking.day = col
	print(booking.day)
	booking.time = row
	booking.date = val
	booking.save()

	return HttpResponse("success")



@csrf_exempt
def upload_documents(request):
	startup = Startup.objects.get(user__user_id=request.user.id)
	startups = Startup.objects.all()

	documents = Documents.objects.all()
	
	if request.method =="GET":
		return render(request, 'startup/uploaddocs.html',{'errormessage':'',
														  'startup':startup,
														  'accepted':"true"})
	else:
		startup = Startup.objects.get(user__user_id=request.user.id)
		document = Documents()
		document.category = "document"
		document.typ = "startup"
		document.title = request.POST.get('title',False)
		document.startup_id = startup.id
		document.doc = request.FILES.get('document',False)
		
		document.save()
		request.session["message"] = "Document added successfully !"
		return redirect('/startup/my_documents')

def show_milestones(request):
	print("asd")
	startup = Startup.objects.get(user__user_id=request.user.id)
	milestones = Milestones.objects.filter(startup_id=startup.id)
	
	for milestone in milestones:
		milestone.deadline = datetime.strptime(str(milestone.deadline), '%Y-%m-%d').strftime('%d/%m/%Y')
		print(milestone.deadline)
	num = len(milestones)/2
	return render(request,"startup/timeline.html",{'startup':startup,'milestones':milestones,'msg':'','accepted':"true"})

def complete_milestone(request,pk):
	print("tets")
	startup = Startup.objects.get(user__user_id=request.user.id)

	milestone = Milestones.objects.get(id=pk)
	print(milestone)
	print("adasdasdasdas")
	milestone.completed_startup	 = 1
	milestone.startup_id = startup.id
	milestone.startup_date = datetime.now()
	milestone.save()
	print(milestone.started)
	return redirect("/startup/show_milestones")


def my_documents(request):
	msg = ""
	if request.session.get('message', False):
		msg = request.session.get('message')
		del request.session['message']
		print(msg)
	docs = Documents.objects.filter(startup__user__user_id=request.user.id,category="document")
	startup = Startup.objects.get(user__user_id=request.user.id)
	left = int(len(docs)/2)
	
	docs_right = docs[:left]
	docs_left = docs[left:]

	return render(request,"startup/my_documents.html",{'startup':startup,
												  	   'docs_left':docs_left,
												  	   'docs_right':docs_right,
												  	   'msg':msg,
												  	   'accepted':"true"})


									

def notifications(request):
	duration = Rent.objects.filter(startup__user__user_id=request.user.id)[0]
	total =  Rent.objects.filter(startup__user__user_id=request.user.id)
	x = {}
	ans = 0
	for t in total:
		if t.paid == '1':
			ans = ans+1
	x["due"] = str((int(duration.duration)-ans)*3000)
	try:
		inc = Incubation.objects.get(startup__user__user_id=request.user.id)
		if inc.accept == 1:
			x["incubation"] = "you request for incubation has been accepted"
	except:
		pass
	try:
		fun = Fund.objects.get(startup__user__user_id=request.user.id)
		if inc.accept == 1:
			x["fund"] = "you request for fund has been accepted from 36 INC"
	except:
		pass
	try:
		mentor = AssignMentor.objects.get(startup__user__user_id=request.user.id)
		months = mentor.months
		name = mentor.mentor.name
		x["mentor"] =  name +" has been assigned to you for "+ months+" months"
	except:
		pass
	print(x)
	print(len(x))

	return HttpResponse(str(x))		





def mytickets(request):
	tickets = Tickets.objects.filter(startup__user__user_id=request.user.id)
	startup = Startup.objects.get(user__user_id=request.user.id)
	left = int(len(tickets)/2)
	
	
	tickets_left = tickets[left:]
	tickets_right = tickets[:left]

	return render(request,"startup/showtickets.html",{'startup':startup,'tickets_left':tickets_left,'tickets_right':tickets_right,"accepted":"true"})


def see_ticket(request,pk):
	startup = Startup.objects.get(user__user_id=request.user.id)
	ticket = Tickets.objects.get(id=pk)
	return render(request,'startup/ticketdetails.html',{'startup':startup,'ticket':ticket,"accepted":"true"})

@csrf_exempt
def mentor_review(request,pk):
	if request.method == "GET":
		mentor = Mentor.objects.get(id=pk)
		startup = Startup.objects.get(user__user_id=request.user.id)
		return render(request,'startup/mentorreview.html',{'startup':startup,'mentor':mentor,"accepted":"true"})
	else:
		review = Reviews()
		review.mentor_id = pk
		startup = Startup.objects.get(user__user_id=request.user.id)
		review.startup_id = startup.id
		review.by_startup = 1
		review.review = request.POST['title']
		review.description = request.POST['desc']
		review.save()
		request.session['message'] = "your review is saved. Thanks for giving the valuable feedaback."
		return redirect('/startup/dashboard')



