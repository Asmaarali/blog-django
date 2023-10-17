from django.shortcuts import render,redirect
from .models import Room , Topic , Message , User
from .forms import RoomForm , UserForm , MyUserCreationForm
from django.db.models import Q  #for searching many field
#authentication 
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages




# Create your views here.
def index(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    # if q is None:
    #     rooms=Room.objects.all()
    # else:
    #      rooms=Room.objects.filter(topic__name=q)
    # rooms=Room.objects.all()
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    recent_message_activities=Message.objects.all().order_by('-created').filter(room__topic__name__icontains=q)[:5]
    topics=Topic.objects.all()
    topics_dict=[]
    #for removing topic which has nothing
    for topic in topics:
        count_rooms=topic.room_set.all()
        # print(count_rooms)
        if count_rooms.count() == 0:
            topic.delete()
        else:
            topics_dict.append(topic)
            
    context={'rooms':rooms,
             'topics':topics,
             'topics_dict':topics_dict,
             'recent_message_activities':recent_message_activities}
    return render(request,"index.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    # print(room)
    # print(room.name)
    #room & Message has one to many relation and incase you have to whow message of each room then you have to use set like below
    room_messages=room.message_set.all().order_by('created')
    #user & room has many to many relation like many user has many participants in rooms 
    participants=room.participants.all()
    # Check for each participant if they have no messages in the room
    # for participant in participants:
    #     has_messages = Message.objects.filter(room=room, user=participant).exists()
    #     if not has_messages:
    #         # Remove the participant from the room
    #         room.participants.remove(participant)
    #         return redirect('room',pk=room.id)
    #         print(f"Removed {participant.username} from {room.name} as they had no messages.")
    if request.method == 'POST':
        send_message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('convo')
        )
        #adding automatically username to recent activities
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,
             'room_messages':room_messages,
             'participants':participants}
    return render(request,"room.html",context)

@login_required(login_url='login')
def createroom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
            topic_name=request.POST.get('topic').lower()
            topic, created=Topic.objects.get_or_create(name=topic_name)
            Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
            return redirect('/')
        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
            # return redirect('/')
    context={'form':form,
             'form_name':'Create',
             'topics':topics}
    return render(request,"room_form.html",context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    #restrict user to view their own thing
    if request.user != room.host:
        return HttpResponse('You have not permission to view this')
    if request.method == 'POST':
        topic_name=request.POST.get('topic').lower()
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('room',pk=room.id)
        # form =RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('/')
    context={'form':form,
             'form_name':'update',
             'topics':topics,
             'room':room}
    return render(request,"room_form.html",context)  

@login_required(login_url='login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    # print(request.user)
    # restrricting user to view only their own thing
    if request.user != room.host:
        return HttpResponse('You have not permission to view this')
    
    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request,"delete_form_confirmation.html",{'obj':room})


@login_required(login_url='login')
def deletemessage(request,pk):
    message=Message.objects.get(id=pk)
    # print(request.user)
    # restrricting user to view only their own thing
    if request.user != message.user:
        return HttpResponse('You have not permission to view this')
    
    if request.method == 'POST':
        message.delete()
        return redirect('/')
        # Get the HTTP referer URL (previous page)
        # previous_page = request.META.get('HTTP_REFERER')

        # if previous_page:
        #     # Redirect to the previous page
        #     return redirect(previous_page)
        # else:
        #     # If there's no previous page, you can provide a default URL or view name to redirect to
        #     return redirect('/')
    return render(request,"delete_form_confirmation.html",{'obj':message})

def alltopics(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,"all_topics_page.html",{'topics':topics})

def recentactivity(request):
    recent_message_activities=Message.objects.all().order_by('-created')
    return render(request,"recent_activity_page.html",{'recent_message_activities':recent_message_activities})
# !--------------------------------------------------!USER authentication --------------------------------------------------

def registerpage(request):
    form=MyUserCreationForm()
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)   
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"Registered successfully")
            return redirect('login')
        else:
            messages.error(request, "Error during registering")
    return render(request,"login_register_form.html",{'form':form})

def loginpage(request):
    #restrict the user is already login then it should not allowed the login page from url
    if request.user.is_authenticated:
        return redirect('index')

    # --------------
    if request.method == 'POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, "user doesnot exist")
    
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login successfully")
            return redirect('index')
        else:
            messages.error(request, "invalid credential")
    return render(request,"login_register_form.html",{'login_page':'Login'})

def logoutuser(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('index')

def profile(request,pk):
    user=User.objects.get(id=pk)
    # rooms=Room.objects.filter(host__username=user)
    rooms=user.room_set.all().order_by('-created')
    recent_message_activities=user.message_set.all().order_by('-created')
    topics=Topic.objects.all()
    context={'user':user,
             'rooms':rooms,
             'recent_message_activities':recent_message_activities,
             'topics':topics}
    return render(request,"profile.html",context)

def updateprofile(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    return render(request,"update_profile.html",{'form':form})