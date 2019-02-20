from django.shortcuts import render,redirect
from django.http import HttpResponse
from investor.models import Investor
from startup.models import Startup 
from django.views.decorators.csrf import csrf_exempt
from .models import Connections
from login.models import Type

def index(request):
	investor = Investor.objects.get(user__user_id=request.user.id)
	return render(request, 'investor/investorprofile.html',{'investor':investor})

def show_startups(request):
	try:
		investor = Investor.objects.get(user__user_id=request.user.id)
	except:
		return HttpResponse("wrong input")
	startups = Startup.objects.all()
	size = len(startups)
	left = int(size/2)
	startups_left = startups[:left]
	startups_right = startups[left:]
	return render(request, 'investor/startups.html',{'investor':investor,'startups_left':startups_left,'startups_right':startups_right})

@csrf_exempt
def update(request):

	investor = Investor.objects.get(user__user_id=request.user.id)
	if request.method == "GET":
		return render(request, 'investor/investorupdate.html',{'investor':investor})
	else:
		investor.investment_range = request.POST['investment']
		investor.description = request.POST['aboutme']
		investor.expertise = request.POST['type']
		image = request.FILES.get('image',False)
		if image is not False:
			startup.image = image
		investor.phone_number = request.POST['phoneno']
		investor.save()
		return redirect('/investor')

# def show_connections(request):
# 	connections = Connections.objects.filter(sentfrom_id=request.user.id)
# 	connection = connections[0]
# 	sentto = connection.sentto
	
# 	typ = Type.objects.get(user_id=sentto.id)
# 	if typ.typ == "investor":
# 		name = Investor.objects.get(user_id=typ.id)
# 		name = name.description

# 	return HttpResponse(str(sentto)+ ' '+str(typ.typ))

def show_connections(request):
	connections1 = Connections.objects.filter(sentfrom_id=request.user.id,accept=True)
	print(len(connections1))
	connections2 = Connections.objects.filter(sentto_id=request.user.id,accept=True)
	print(len(connections1))
	startups = []
	for connection in connections1:
		sentto = connection.sentto
		typ = Type.objects.get(user_id=sentto.id)
		if typ.typ == "startup":
			print("got1")
			name = Startup.objects.get(user_id=typ.id)
			print(name.description)
			startups.append(name)
			print(startups)
	for connection in connections2:
		sentfrom = connection.sentfrom
		typ = Type.objects.get(user_id=sentfrom.id)
		if typ.typ == "startup":
			name = Startup.objects.get(user_id=typ.id)
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
	investor = Investor.objects.get(user__user_id=request.user.id)
	return render(request, 'investor/myconnections.html',{'investor':investor,'startups_left':startups_left,'startups_right':startups_right})


def show_pending_connections(request):
	connections2 = Connections.objects.filter(sentto_id=request.user.id,response=False)
	
	startups = []
	for connection in connections2:
		sentfrom = connection.sentfrom
		typ = Type.objects.get(user_id=sentfrom.id)
		if typ.typ == "startup":
			name = Startup.objects.get(user_id=typ.id)
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
	investor = Investor.objects.get(user__user_id=request.user.id)
	return render(request, 'investor/mypendingconnections.html',{'investor':investor,'startups_left':startups_left,'startups_right':startups_right})

def accept_connection(request,pk):
	print("das")
	investor = Investor.objects.get(user__user_id=request.user.id)
	try:
		startup = Startup.objects.get(id=pk)
		num = startup.user.user.id
		connection = Connections.objects.get(sentto_id=request.user.id,sentfrom_id=num) 
	except:
		return HttpResponse("error")
	connection.response = True
	connection.accept = True
	connection.save()
	return redirect("/investor/show_pending_connections")

def reject_connection(request,pk):
	investor = Investor.objects.get(user__user_id=request.user.id)

	print("\n",pk)
	startup = Startup.objects.get(id=pk)
	num = startup.user.user.id
	print(num)
	connection = Connections.objects.get(sentto_id=request.user.id,sentfrom_id=num) 
	
	connection.response = True
	connection.accept = False
	connection.save()
	return redirect("/investor/show_pending_connections")