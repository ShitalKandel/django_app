from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, UserImageForm, NewPostForm, FriendRequestForm
from .models import UserProfile, FriendRequest
from django.http import JsonResponse



@login_required
def register(request):
    # username = None  
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']  
            # UserProfile.objects.create_user(email='email', password='password')  
            form.save()
            return redirect('web_app:login_success')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form':form,})


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
                return redirect('web_app:login_success')
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
    # if FriendRequest.objects.filter(id=request.user_id).exists():
    # try:
        # friend_list = FriendRequest.objects.get(user_id=request.user_id)
    # except FriendRequest.DoesNotExist:
        # return "the user_id doesn't exists ".format(request.user_id)
    #     # friend_list = None
    # if friend_list in FriendRequest:
    #     friend_list = FriendRequest.objects.filter(to_user=request.user, status=FriendRequest.PENDING)
    #     return render(request, 'toggle.html', {'pending_requests': friend_list})
    return render(request, 'login_success.html',context= {'form': form, 'recommended_users': recommended_users})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('web_app:login_success')  # Redirect to the appropriate page after uploading the image
    else:
        form = NewPostForm()
    return render(request, 'upload_image.html', {'form': form})


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
        to_user_id = request.POST.get('to_user')
        to_user = UserProfile.objects.get(pk=to_user_id)
        existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status=FriendRequest.to_user).exists()
        if existing_request:
            return JsonResponse({'success': False, 'error': 'Friend request already sent'})
        else:
            friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            friend_request.save()
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Friend request does not exist'})

    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        #accepted update
        friend_request.status = FriendRequest.ACCEPTED
        friend_request.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'You are not authorized to accept this request.'})


@login_required
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Friend request does not exist'})

    if friend_request.to_user == request.user:
        friend_request.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'You are not authorized to reject this request.'})


@login_required
def notify(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status=FriendRequest.status)
    notifications = [{'from_user': request.from_user.username, 'id': request.id} for request in pending_requests]
    return JsonResponse(notifications, safe=False)


# @login_required
# def index(request):
#     return render(request,'toggle.html')