from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Rent
from django.views.decorators.csrf import csrf_exempt
from startup.models import Startup
def get_admin(id):
 	admin = User.objects.get(id=id)
 	return admin
@csrf_exempt
def index(request):

	msg = ""
	if request.session.get('message', False):
		msg = request.session.get('message')
		del request.session['message']
		print(msg)


	if request.method == 'GET':
		rents = Rent.objects.filter(curr=True)
		data_upper = [{'1':0},{'2':0}]
		data_lower = [{'3':0},{'4':0}]
		for r in rents:
			for d in data_upper:
				key = list(d.keys())[0]
				print(key)
				if key==r.room_no :
					d[r.room_no] = 1
					d["startup"] = r.startup.name
					d["duration"] = r.duration
					d["image"] = r.startup.image.url
					d["date_alloted"] = r.date_alloted
			for d in data_lower:
				key = list(d.keys())[0]
				print(key)
				if key==r.room_no :
					d[r.room_no] = 1
					d["startup"] = r.startup.name
					d["duration"] = r.duration
					d["image"] = r.startup.image.url
					d["date_alloted"] = r.date_alloted

		print(data_upper)
		startups = Startup.objects.all()
		data = []
		occupied = []
		for r in rents:
			occupied.append(r.startup.id)
		for s in startups:
			if s.id not in occupied:	
				temp = {"startup": s.name}
				data.append(temp)

		print(data)
		return render(request,'rent/rentmap.html',{	'data_upper':data_upper,
													'data_lower':data_lower,
													'admin':get_admin(request.user.id),
													'startups':data,
													'msg':msg
													})
	else:
		startupName = request.POST.get('startup')
		room_no = request.POST.get('roomno')
		duration = request.POST.get('duration')
		rent = Rent()
		startup = Startup.objects.get(name=startupName)
		rent.startup_id = startup.id
		rent.duration = duration
		rent.curr = True
		rent.room_no = room_no
		rent.month = 1
		rent.save()
		request.session['message'] = "Room Alloted !"
		print("Room alloted")
		return redirect('/rent')

def give_rent(request):
	return render(request,'rent/rentmap.html',{'admin':get_admin(request.user.id)})

def pay_rent(request):
	startup = Startup.objects.get(user__user_id=request.user.id)
	return render(request,'rent/rentpay.html',{'startup':startup})