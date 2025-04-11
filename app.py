from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm

User = get_user_model()

# Store verification codes temporarily (in production, use cache or database)
verification_codes = {}

# Forms
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm new password'
        })
    )

class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter verification code'
        })
    )

# Views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate verification code
                code = get_random_string(length=6, allowed_chars='0123456789')
                verification_codes[email] = {
                    'code': code,
                    'user_id': user.id
                }
                
                # Send verification code via email
                send_mail(
                    'Password Reset Verification Code',
                    f'Your verification code is: {code}',
                    'noreply@medireminder.com',
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Verification code has been sent to your email.')
                return redirect('users:verify_code')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'users/password_reset.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            # Find the email with matching verification code
            for email, data in verification_codes.items():
                if data['code'] == code:
                    user = User.objects.get(id=data['user_id'])
                    token = default_token_generator.make_token(user)
                    # Clear the verification code
                    del verification_codes[email]
                    return redirect('users:password_reset_confirm', uidb64=user.id, token=token)
            
            messages.error(request, 'Invalid verification code.')
    else:
        form = VerificationCodeForm()
    
    return render(request, 'users/verification_code.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        user = User.objects.get(id=uidb64)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('users:password_reset_complete')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')
        return redirect('users:password_reset')

def password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def doctor_list(request):
    doctors = Doctor.objects.filter(user=request.user)
    return render(request, 'users/doctor_list.html', {'doctors': doctors})

@login_required
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user
            doctor.save()
            messages.success(request, 'Doctor has been added successfully!')
            return redirect('users:doctor_list')
    else:
        form = DoctorForm()
    
    return render(request, 'users/doctor_form.html', {
        'form': form,
        'action': 'Add'
    })

@login_required
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor information has been updated!')
            return redirect('users:doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'users/doctor_form.html', {
        'form': form,
        'doctor': doctor,
        'action': 'Edit'
    })

@login_required
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, user=request.user)
    
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor has been deleted successfully!')
        return redirect('users:doctor_list')
        
    return render(request, 'users/doctor_confirm_delete.html', {'doctor': doctor})
