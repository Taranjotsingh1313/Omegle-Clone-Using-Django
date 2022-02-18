from django.shortcuts import redirect, render
from .models import Waiting,Connected,GroupModel
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
import random
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request,'index.html')

def createMatch(request):
    # CHECKING IF USER PRESENT IN THE USER1 AND USER2 IN CONNECTED
    User1_Checking = Connected.objects.filter(user_1=request.user)
    User2_Checking = Connected.objects.filter(user_2=request.user)
    if User1_Checking:
        print("user1 checking")
        # Getting The Group Name
        group_name = User1_Checking[0].user_1.username + User1_Checking[0].user_2.username
        # getting the model from the group to check
        group_model = GroupModel.objects.filter(group=group_name)
        if group_model.count() == 0:
            # creating group object
            group_create = GroupModel.objects.create(group=group_name)
            group_create.users.add(request.user)
            return redirect(f"/video/{group_name}/created")
        else:
            group_model[0].users.add(request.user)
            return redirect(f"/video/{group_name}/join")


        
    elif User2_Checking:
        print("user2 checking")
        # Getting The Group Name
        group_name = User2_Checking[0].user_1.username + User2_Checking[0].user_2.username
        # getting the model from the group to check
        group_model = GroupModel.objects.filter(group=group_name)
        if group_model.count() == 0:
            # creating group object
            group_create = GroupModel.objects.create(group=group_name)
            group_create.users.add(request.user)
            return redirect(f"/video/{group_name}/created")
        else:
            group_model[0].users.add(request.user)
            return redirect(f"/video/{group_name}/join")
        
    else:
        # random user
        random_user_list = list(Waiting.objects.all())
        if len(random_user_list) > 1:
            random_user = random.choice(random_user_list)
        else:
            Waiting.objects.filter(user=request.user).delete()
            messages.success(request,"Please Try Again Later No One Is Online And Follow The Steps Again!")
            return redirect("index")
        if random_user.user == request.user :
            Waiting.objects.filter(user=request.user).delete()
            messages.success(request,"Please Try Again Later No One Is Online And Follow The Steps Again!")
            return redirect("index")
        else:
        # add them to the connected model
            connected_add = Connected.objects.create(user_1=request.user,user_2=random_user.user)
            Waiting.objects.filter(user=request.user).delete()
            Waiting.objects.filter(user=random_user.user).delete()
            messages.success(request,"Founded The Stranger Please Click Again")
            return redirect("index")

def register(request):
    # CHECKING USER IF USER ALREADY EXISTS IN THE WAITING MODEL
    CheckingWaiting = Waiting.objects.filter(user=request.user)
    if CheckingWaiting:
        messages.error(request,'Server Finding Stranger Please Click On The Check ')
        return redirect("index")
    # ADDING USER TO THE WAITING MODEL
    AddingToWaiting = Waiting.objects.create(user=request.user)
    messages.error(request,'Now Server Knows You Please Click On Check After Every 5 Seconds')
    return redirect("index")

def videoChat(request,groupname,created):
    if not request.user.is_authenticated:
        return redirect("login")
    groupname = groupname
    
    return render(request,'video.html',{'groupname':groupname,'created':created})

# Login View
def Login(request):
    if request.user.is_authenticated:
        return redirect("index")    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('index')
    return render(request,'login.html')

# Signup View
def SignUp(request):
    if request.user.is_authenticated:
        return redirect("index") 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # checking if the user exists or not
        user_check = User.objects.filter(username=username)
        if user_check:
            messages.error(request,"Username Already Exists")
            return redirect("signup")
        user = User.objects.create_user(username=username,password=password)
        if user:
            return redirect('login')
    return render(request,'signup.html')
# Logout
def Logout(request):
    logout(request)
    return redirect("login")

# skipping the user
def Skip(request,groupname):
    try:
        # fetching the connected object of user
        connected_user = Connected.objects.filter(user_1=request.user) or Connected.objects.filter(user_2=request.user)
        # adding both users again in the waiting 
        connected_user.delete()
        group_model = GroupModel.objects.filter(group=groupname)
        group_model.delete()
        return redirect("index")
    except :
        group_model = GroupModel.objects.filter(group=groupname)
        group_model.delete()
        return redirect('index')