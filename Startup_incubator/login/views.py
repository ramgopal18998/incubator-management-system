from django.shortcuts import render
from startup.models import Startup,Founder
from .models import Type
from investor.models import Investor
from mentor.models import Mentor
from django.contrib.auth.models import User
from investor.models import Investor
from mentor.models import Mentor
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
# Create your views here.

@csrf_exempt
def register(request):
	if request.method =='GET':
		return render(request,'front/register.html')
	else:
		name = request.POST['name']
		founder_name = request.POST.get('founder_name')
		founder_email = request.POST.get('founder_email')
		founder_phone = request.POST.get('founder_phone')
		founder_address = request.POST.get('founder_address')
		#dipp = request.POST['dipp']
		address = request.POST['address']
		typ = request.POST['type']
		email = request.POST['email']
		description = request.POST['description']
		mobile = request.POST['mobile']
		password = request.POST['password']

		
		image = request.FILES.get('image',False)
		print(image)
		user = User()
		user.username = name
		user.set_password(password)
		user.email = email
		user.is_active = True

		## for admin easy access
		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		### end

		user.save()
		cat = Type()
		user1 = User.objects.get(username=name)
		cat.user_id  = user1.id
		cat.save()
		founder = Founder()
		founder.name = founder_name
		founder.email = founder_email
		founder.phone_number = founder_phone
		founder.address = founder_address
		founder.save()
		startup = Startup()
		user1 = Type.objects.get(id=cat.id)
		startup.user_id = user1.id
		startup.name = name
		startup.address = address
		startup.email = email
		#startup.dipp = dipp
		f1 = Founder.objects.get(id=founder.id)
		startup.founder_id = f1.id
		startup.description = description
		startup.phone_number = mobile
		print(image)
		if image is not False:
			startup.image = image
		startup.cat = typ
		startup.save()
		logout(request)
		return redirect("/login/")



@csrf_exempt
def login_user(request):
	if request.method =='GET':
		if not request.user.is_authenticated():
			return render(request,'front/login.html')
		else:
			return redirect("/startup/")
	else:
		email = request.POST['email']
		password = request.POST['password']
			
		try:
			print(email)
			user = User.objects.get(email=email)
			print(user.username)
			user = authenticate(username=user.username, password=password)
		except:
			return render(request, 'front/login.html', {'error_message': 'Incorrect Credentials'})
		if user is not None:
			if user.is_active:
				login(request,user)
				print("logged in")
				user1 = Type.objects.get(user_id=user.id)
				if user1.typ == "startup":
					startup = Startup.objects.get(user_id=user1.id)
					return redirect("/startup/")
				if user1.typ == "investor":
					startup = Investor.objects.get(user_id=user1.id)
					return redirect('/investor/')
				if user1.typ == "mentor":
					startup = Mentor.objects.get(user_id=user1.id)
					return redirect('/mentor')
			else:
				return render(request, 'front/login.html', {'error_message': 'Your account has been disabled'})

		else:
			return render(request, 'front/login.html', {'error_message': 'Invalid login'})




def home(request):
	print("yes")
	return render(request,"front/index.html")





