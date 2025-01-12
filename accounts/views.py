from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Referral, Profile, ProductScheme, Services
from .forms import ProductSchemeForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
import random
import string
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from decimal import Decimal
from datetime import datetime, timedelta

# View to handle Product Scheme Management
# def product_scheme_manage(request):
#     product_id = request.GET.get('id')
#     total = request.GET.get('total')

#     if request.method == 'POST':
#         form = ProductSchemeForm(request.POST)
#         if form.is_valid():
#             scheme = form.save(commit=False)
#             scheme.start_date = datetime.now()
#             scheme.end_date = scheme.start_date + timedelta(days=form.cleaned_data['days'])
#             scheme.save()
#             return redirect('payment_screen')
#         else:
#             print(f"Form errors: {form.errors}")  # Debugging line
#     else:
#         form = ProductSchemeForm(initial={'product_id': product_id, 'total': total})

#     return render(request, 'product_scheme_manage.html', {
#         'form': form,
#         'product_id': product_id,
#         'total': total
#     })

def payment_screen(request):
    return render(request, 'payment.html')

def generate_referral_code():
    """Generate a unique 8-character referral code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect authenticated users to home

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create profile with referral code and save KYC details
            referral_code = generate_referral_code()
            referred_by = request.POST.get('referred_by', None)

            referred_by_profile = None
            if referred_by:
                try:
                    referred_by_profile = Profile.objects.get(referral_code=referred_by)
                except Profile.DoesNotExist:
                    referred_by_profile = None

            profile = Profile.objects.create(
                user=user,
                referral_code=referral_code,
                referred_by=request.POST.get('referred_by', None),
                kyc_document=form.cleaned_data.get('kyc_document'),
                kyc_document_type=form.cleaned_data.get('kyc_document_type'),
                pan_card=form.cleaned_data.get('pan_card'),
                bank_passbook=form.cleaned_data.get('bank_passbook'),
            )

            # Track referral and rewards
            if referred_by_profile:
                referred_by_profile.referrals_made += 1
                referred_by_profile.rewards_earned += 10.00  # Example reward
                referred_by_profile.save()
                Referral.objects.create(referred_by=referred_by_profile, referred_user=user)

            auth_login(request, user)
            messages.success(request, "Signup successful! Welcome aboard!")
            return JsonResponse({'success': True, 'referral_code': referral_code})

        else:
            # Process form errors and send them as JSON response
            errors = {
                field: [error['message'] for error in error_list]
                for field, error_list in form.errors.get_json_data().items()
            }
            return JsonResponse({'success': True, 'referral_code': referral_code})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Login successful! Welcome back!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    # Fetch user profile data
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    dict_eve = {
        'post': Post.objects.all()
    }
    return render(request, 'index.html', dict_eve)

def about(request):
    return render(request, 'about.html')


def terms(request):
    return render(request, 'terms.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def refar(request):
    return render(request, 'refar.html')


def services_view(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})

@login_required
def referral_view(request):
    user_profile = Profile.objects.get(user=request.user)

    # Generate referral code if not already set
    if not user_profile.referral_code:
        user_profile.referral_code = generate_referral_code()

    # Fetch referral details
    referrals = Referral.objects.filter(referred_by=user_profile)
    referral_count = referrals.count()
    total_rewards = user_profile.rewards_earned

    # Collect referred persons' details
    referred_persons = [
        {
            'name': referral.referred_user.username,
            'timestamp': referral.timestamp,
        }
        for referral in referrals
    ]

    context = {
        'referral_code': user_profile.referral_code,
        'referral_count': referral_count,
        'total_rewards': total_rewards,
        'referred_persons': referred_persons,
    }
    return render(request, 'refar.html', context)




def product_scheme_manage(request):
    product_id = request.GET.get('id')
    total = request.GET.get('total')
    
    if product_id:
        # Fetch the product info based on ID
        try:
            post = Post.objects.get(id=product_id)
        except Post.DoesNotExist:
            post = None
            total = None

    if request.method == 'POST':
        form = ProductSchemeForm(request.POST)
        if form.is_valid():
            scheme = form.save(commit=False)
            scheme.start_date = datetime.now()
            scheme.end_date = scheme.start_date + timedelta(days=form.cleaned_data['days'])
            scheme.save()
            return redirect('payment_screen')
        else:
            print(f"Form errors: {form.errors}")  # Debugging line
    else:
        form = ProductSchemeForm(initial={'product_id': product_id, 'total': total})

    return render(request, 'product_scheme_manage.html', {
        'form': form,
        'product_id': product_id,
        'total': total,
        'post': post
    })
