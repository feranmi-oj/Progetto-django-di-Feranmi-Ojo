from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,UserEditForm,ProfileEditForm,LoginForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .models import Profile
from articles.models import Article

# Create your views here.

@login_required()
def ip_control_view(request):
    context = {}
    return render(request, 'registration/ip_control.html', context)

def getIpAdd(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def login_view(request):
    ip_address = getIpAdd(request)
    initial_data = {
        'ip_address': ip_address,
    }
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            try:
                user_info = Profile.objects.get(user=user)
            except:
                user_info = Profile.objects.create(user=user)
            user_info.save()
            ip_address = getIpAdd(request)
            if ip_address != user_info.ip_address:
                user_info.ip_address = ip_address
                user_info.save()
                return redirect(f"/ip_control/?next={next}")

            else:
                return redirect('blog/')
    else:
        form = LoginForm(initial=initial_data)
    return render(request, 'registration/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() #stiamo andando a ricaricare l'istanza del profilo che è stata generata dal signals
            user.profile.birthday = form.cleaned_data.get('birthday')
            user.profile.ip_address= getIpAdd(request)
            user.profile.save()
            username = form.cleaned_data.get('username')
            row_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username,password=row_password)
            login(request,user)
            return redirect('accounts:profile', id=user.id)
    else:
        form = RegistrationForm()
    return render(request,'registration/registration.html',{'form':form})
def num_post(request):
    num_post = Article.objects.filter(author=request.user)
    return render(request, 'some_template.html', {'num_post': num_post})

def profile(request,id):
    user_profile = get_object_or_404(Profile, id=id)
    num_post = Article.objects.filter(author=request.user)
    return render(request, 'accounts/profile.html', {'user_profile': user_profile,'num_post':num_post})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return render(request,'accounts/profile_change_done.html')
        else:
            messages.error(request,'The data entered is not valid',extra_tags='danger')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'registration/edit.html',
                  {'user_form': user_form,'profile_form': profile_form})
