from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User

from .forms import PostForm, RegistrationForm
from .models import Post

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'main/home.html'
    login_url = '/login/'

def sign_up(request):

    if request.method =='POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse(viewname='main:home'))
    
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign-up.html', { "form" : form })

@permission_required('main.add_post', raise_exception=True)
@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse(viewname='main:home'))
        
    else:
        form = PostForm()
    
    return render(request, 'main/create-post.html', { "form" : form })
   

@login_required
def delete_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.filter(id=post_id).first()

    if post and (post.user == request.user or request.user.has_perm('main.delete_post')):
        post.delete()
    
    return redirect(reverse('main:home'))

def ban_user(request):

    user_id = request.POST.get("user_id")
    user = User.objects.filter(id=user_id).first()

    print(f"user ban: {user}")
    if user and request.user.is_superuser:


        try:
            default_group = Group.objects.filter(name='default').first()
            default_group.user_set.remove(user)
        except:
            pass
        
        try:
            mod_group = Group.objects.filter(name='mod').first()
            mod_group.user_set.remove(user)
        except:
            pass

    return redirect(reverse('main:home'))