from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from users.models import User
from users.forms import CustomUserCreationForm
from users.services.services import (
    follow_user,
    unfollow_user,
    is_following_user,
    get_followers_count,
    get_following_count,
)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(User, username = username)

    is_following = (
        request.user.is_authenticated 
        and request.user != profile_user 
        and is_following_user(request.user.id, profile_user.id)
    )
        
    followers_count = get_followers_count(profile_user.id)
    following_count = get_following_count(profile_user.id)

    questions = profile_user.questions.all().order_by('-timestamp')
    
    for question in questions:
        question.set_vote_status(request.user.id)
    
    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'questions': questions,
    }

    return render(request, 'users/profile.html', context)

@login_required
@require_POST
def follow_user_view(request, target_id):
    follow_user(request.user.id, target_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
@require_POST
def unfollow_user_view(request, target_id):
    unfollow_user(request.user.id, target_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
