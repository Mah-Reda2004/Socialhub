from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

import random

from .forms import RegisterForm, ProfileForm
from posts.models import Post
from core.utils import send_welcome_email

# ------------------------
# Registration
# ------------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            # Update automatically created profile
            profile = user.profile
            updated_profile = profile_form.save(commit=False)
            profile.bio = updated_profile.bio
            profile.avatar = updated_profile.avatar
            profile.location = updated_profile.location
            profile.birth_date = updated_profile.birth_date
            profile.save()

            login(request, user)
            messages.success(request, "Account created successfully ✅")
            return redirect("home")
        else:
            messages.error(request, "There was an error with your submission ❌")
    else:
        form = RegisterForm()
        profile_form = ProfileForm()

    return render(request, "account/register.html", {"form": form, "profile_form": profile_form})


# ------------------------
# Account activation
# ------------------------
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! Please log in.")
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("register")


# ------------------------
# Login & Logout
# ------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("feed")
            else:
                messages.error(request, "Account is not active. Check your email.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------------
# Profile Settings
# ------------------------
@login_required
def profile_settings(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/settings.html", {"form": form})


# ------------------------
# Password Reset
# ------------------------
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "This email is not registered.")
            return redirect("password_reset_request")

        reset_code = str(random.randint(100000, 999999))
        request.session["reset_code"] = reset_code
        request.session["reset_email"] = email

        subject = "Password Reset Code"
        from_email = settings.DEFAULT_FROM_EMAIL
        message = f"Your password reset code is: {reset_code}"

        html_message = render_to_string(
            "account/password_reset_email.html", {"reset_code": reset_code}
        )

        send_mail(subject, message, from_email, [email], html_message=html_message)
        messages.success(request, "A reset code has been sent to your email.")
        return redirect("password_reset_confirm")

    return render(request, "account/password_reset_request.html")


def password_reset_confirm(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        code_sent = request.session.get("reset_code")

        code_entered = request.POST.get("reset_code")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if code_entered != code_sent:
            messages.error(request, "Invalid reset code.")
            return redirect("password_reset_confirm")

        if new_password1 != new_password2:
            messages.error(request, "Passwords do not match.")
            return redirect("password_reset_confirm")

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password1)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "Error: Email not found.")

    return render(request, "account/password_reset_confirm.html")


# ------------------------
# Profile View
# ------------------------
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-created_at")
    return render(
        request, "account/profile.html", {"profile_user": user, "posts": posts}
    )


# ------------------------
# Delete Post
# ------------------------
from django.http import HttpResponseForbidden

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully ✅")
        return redirect("feed")
