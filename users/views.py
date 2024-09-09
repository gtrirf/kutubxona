from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import CustomUser, VerificationCode

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == 'POST':
        code = request.POST.get('verification_code')
        verification_code = VerificationCode.objects.filter(code=code, is_active=True).first()
        if verification_code and verification_code.is_valid():
            user = verification_code.user
            login(request, user)
            verification_code.is_active = False
            verification_code.save()
            return redirect('home:home')
        else:
            return render(request, 'login.html', {'error': 'Invalid or expired verification code.'})
    return render(request, 'login.html')


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('home:home')