from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room, Message
from django.http import HttpResponse, JsonResponse

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "chat/chatPage.html")

def room(request, room_name):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room_name)
    return render(request, "chat/chatRoom.html", {
        'username': username,
        'room_name': room_name,
        'room_details': room_details
    })

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def getMessages(request, room_name):
    room_details = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            # elif User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email Taken')
            #     return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    else:
        return render(request, 'chat/RegisterPage.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'chat/LoginPage.html')

def logout(request):
    auth.logout(request)
    return redirect('login')