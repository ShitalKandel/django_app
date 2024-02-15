from django.shortcuts import render, redirect
from django.contrib.auth import  login,authenticate
from .models import UserProfile,ImageForm, Feeds
from .forms import SignupForm,LoginForm,UserImage,New_post
from django.contrib.auth.mixins import LoginRequiredMixin


'''
register a account using django form
'''
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()   
            return redirect('web_app:login_success')  
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


'''
after logging in it will redirect to a new page
'''
def login_success(request):
    form = UserImage(request.POST, request.FILES)
    print("Hello")
    if form.is_valid():
        form = form.save
    
    recommended_users = UserProfile.objects.exclude(id=request.user.id)
    return render(request, 'login_success.html',{'form':form,'recommended_users':recommended_users})


'''
it verifies the user and redirects to login_success 
if the user is valid
'''
def signIn(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            user= UserProfile.objects.filter(email=email,password=password).first()  #check if userprofile exists or not (only single userprofile)
            if user:
                login(request=request,user=user)
                return redirect('web_app:login_success')
            else:
                error_message = "Invalid username or password."
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})


"""
it redirects to the login_success
"""
def profile(request):
    return redirect(request,'login_success')


'''
User logout form login_success page
'''
def logout(request):
    
    return render(request,'logout.html')



'''
it uplods the image
'''
def upload_image(request,image_id):
    try:
        image = ImageForm.objects.get(pk=image_id)
    
    except ImageForm.DoesNotExist:
        return redirect('image not found')
    
    if request.method == 'POST':
        form = UserImage(request.POST,request.FILES,instance=image)
        if form.is_valid():
            form.save()
            return render('user_post.html')
    else:
        form = UserImage(instance=image)
        return render(request,'image.html',{'form':form,'image':image})
    

'''
creating a post on the login_success page'''
def create_post(request):
    if  request.method =="POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = request.user
            post.save()
        return redirect(request,'post')
    else:
        form = create_post()
        return render(request,'login_success',{'form':form})



'''
this field is created to upload image with caption
'''
def image_request(request):
    form = UserImage()
    if request.method == 'POST':
        form = UserImage(request.POST, request.FILES)    
        if form.is_valid():
            image = form.save()
            return render(request,'image.html',{'image':image})
    else:
        form = UserImage()

    return render(request,'image.html',{'form':form})



'''
displays the created post on feeds of the page
with the username , comment , number of likes ,caption or image
'''
def post(request, first_name, last_name ):
    user = UserProfile.objects.get(first_name=first_name, last_name=last_name)
    if request.method == 'POST':
        form = New_post(request.POST,request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = user
            feed.save()
            return redirect(f'/{user.first_name}_{user.last_name}/')

    else:
        form = New_post()

    feeds = Feeds.objects.filter(user=user)
    return render(request, 'user_post.html', {'user': user, 'feeds': feeds, 'form': form})



'''profiel bar '''
def left_Profile_Bar(request):
    users = UserProfile.objects.all()

    return render(request,'left_side_profilebar.html' ,{'users':users})


'''settings bar'''
def right_Profile_Bar(request):
    return render(request,'right_side_profilebar.html' )