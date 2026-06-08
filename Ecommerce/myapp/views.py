from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Topic, Message, Room
from .forms import RoomForm,UserForm,User,MyUserCreationForm


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=email, password=password)
        except Exception as e:
            messages.error(request, 'A server error occurred during authentication.')
            return redirect('login')

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    context = {'page': page}
    return render(request, 'myapp/register-login.html', context)


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # normalize username and email to avoid case-sensitivity issues
            if getattr(user, 'username', None):
                user.username = user.username.lower()
            if getattr(user, 'email', None):
                user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Surface form validation errors to the user
            for field, errors in form.errors.items():
                for err in errors:
                    # use field name for field-specific errors, otherwise show non-field errors
                    if field == '__all__':
                        messages.error(request, f"Error: {err}")
                    else:
                        messages.error(request, f"{field}: {err}")
            # also include non-field errors if present
            for err in form.non_field_errors():
                messages.error(request, f"Error: {err}")
    return render(request, 'myapp/register-login.html', {'form': form, 'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def rooms(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all().order_by('-created_at')
    participants=room.participants.all()
    if request.method == 'POST':
        message_body = request.POST.get('body')
        if message_body:  # Ensure message body is not empty
            Message.objects.create(
                user=request.user,
                room=room,
                body=message_body,
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'myapp/Room.html', context)


def django_page(request):
    posts = Post.objects.all()
    return render(request, 'myapp/DjangoPage.html', {'posts': posts})


@login_required(login_url='login')
def home(request):
    topics = Topic.objects.all()[0:5]
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'myapp/home.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()  # Initialize the form
    topics = Topic.objects.all()  # Fetch all topics

    if request.method == 'POST':
        topic_name = request.POST.get('topic')  # Get the topic name from the POST request
        room_name = request.POST.get('name')  # Get the room name
        description = request.POST.get('description')  # Get the room description

        # Ensure that the topic name, room name, and description are provided
        if not topic_name or not room_name or not description:
            messages.error(request, 'All fields are required.')
            return render(request, 'myapp/CreateRoom.html', {'form': form, 'topics': topics})

        # Create or get the topic
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # Create the room
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=room_name,
            description=description
        )

        messages.success(request, 'Room created successfully.')
        return redirect('home')  # Redirect to the home page or another appropriate view

    context = {'form': form, 'topics': topics}  # Prepare context for rendering
    return render(request, 'myapp/CreateRoom.html', context)  # Render the template

def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    room_message=user.message_set.all()
    context={'user':user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request,'myapp/profile.html',context)


@login_required(login_url='login')
def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room.')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form,'topics': topics,'room': room}
    return render(request, 'myapp/CreateRoom.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponse('You are not authorized to delete this room.')

    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully.')
        return redirect('home')

    return render(request, 'myapp/DeleteRoom.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    # Check if the user is authorized to delete the message
    if request.user != message.user:
        return HttpResponse('You are not authorized to delete this message.',
                            status=403)  # Return a 403 Forbidden status

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('home')

    return render(request, 'myapp/deleteRoom.html', {'obj': message})

@login_required(login_url='login')
def update_user(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
           form.save()
           return redirect('profile',pk=user.id)
    return render(request, 'myapp/update_user.html', {'form': form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'myapp/topics.html',{'topics':topics})

def activityPage(request):
    room_messages=Message.objects.all()
    return render(request,'myapp/activity.html', {'room_messages': room_messages})
