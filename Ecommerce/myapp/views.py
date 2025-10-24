from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Topic, Message, Room
from .forms import RoomForm


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    context = {'page': page}
    return render(request, 'myapp/register-login.html', context)


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
    return render(request, 'myapp/register-login.html', {'form': form})


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
    topics = Topic.objects.all()
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
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # Set the host to the current user
            room.save()
            messages.success(request, 'Room created successfully.')
            return redirect('home')
    context = {'form': form}
    return render(request, 'myapp/CreateRoom.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room.')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully.')
            return redirect('home')
    context = {'form': form}
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

    return render(request, 'myapp/DeleteMessage.html', {'obj': message})
