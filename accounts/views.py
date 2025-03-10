from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.http import HttpResponse

@login_required
def Home(request):
    return render(request, "index.html")

def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username Already exists")
        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request, "Useremail Already exists")
        if len(password) < 5:
            user_data_has_error=True
            messages.error(request, "Password should greater than 5 characters")
        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account register successfully!")
            return redirect('login')
    return render(request, "register.html")

def LoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid user or password")
            return redirect('login')
    return render(request, "login.html")

def LogoutView(request):
    logout(request)
    return redirect('login')

def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id':new_password_reset.reset_id})
            complete_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            email_body = f"Reset your password by this link given bleow: /n/n/n {complete_password_reset_url}"

            email_message = EmailMessage(
                "Reset password request",
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_message.fail_silently = False
            email_message.send()
            

            return redirect('password-reset-send', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"User email '{email}' not found")
            return redirect('forget-password')
    return render(request, 'forget_password.html')

def PasswordResetSend(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
         return render(request, 'password_reset_send.html')
    else:
        messages.error(request, "Invalid reset id")
        return redirect('forget-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method == 'POST':
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]

            password_error = False
            if new_password != confirm_password:
                password_error =True
                messages.error(request, "Password does not match")
            if len(new_password) < 5:
                password_error = True
                messages.error(request, "Password field must contains more than 5 characters")

            expiration_time = password_reset_id.created_at + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                password_error = True
                messages.error(request, "Reset link expired")

            if not password_error:
                user = password_reset_id.user
                user.set_password(new_password)
                user.save()
                reset_id = get_object_or_404(PasswordReset, reset_id=reset_id)  # Fetch object

                reset_id.delete()  # Now this will work correctly

                messages.success(request, "Password reset successfully , now back to login")
                return redirect('login')
            else:
                return redirect('reset-password', reset_id=reset_id)
    except PasswordReset.DoesNotExist:
        messages.error(request, "Invalid reset id")
        return redirect('forget-password')
    return render(request, 'reset_password.html')