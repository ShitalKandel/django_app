from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, UserImageForm, NewPostForm, FriendRequestForm
from .models import UserProfile, FriendRequest


@login_required
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # Access the username field
            form.save()
            return redirect('web_app:login_success')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})

@login_required
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('login_success')
            else:
                error_message = "Invalid email or password."
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')


@login_required
def login_success(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('web_app:login_success')
    else:
        form = UserImageForm()
    recommended_users = UserProfile.objects.exclude(id=request.user.id)
    return render(request, 'login_success.html', {'form': form, 'recommended_users': recommended_users})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('login_success')
    else:
        form = UserImageForm()
    return render(request, 'image.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('login_success')
    else:
        form = NewPostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})


@login_required
def add_friend(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.from_user = request.user
            friend_request.save()
            return redirect('login_success')
    else:
        form = FriendRequestForm()
    return render(request, 'add_friend.html', {'form': form})


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        return HttpResponse('You are not authorized to accept this request.')


@login_required
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return HttpResponse('Friend request rejected')
    else:
        return HttpResponse('You are not authorized to reject this request.')
