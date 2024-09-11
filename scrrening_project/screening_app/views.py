from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm,CustomAuthenticationForm,ResumeUploadForm
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(mail_subject, message, '21uad020@kamarajengg.edu.in', [user.email])
            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True  # Assuming you have an 'email_verified' field in your model
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'account_activation_invalid.html')
    
# views.py

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    if user.user_type == 'employer':
                        return redirect('employer_dashboard')  # Redirect to the employer's dashboard
                    elif user.user_type == 'applicant':
                        return redirect('applicant_dashboard')  # Redirect to the applicant's dashboard
                    else:
                        messages.error(request, 'User type not recognized.')
                else:
                    messages.error(request, 'Please verify your email address before logging in.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def employer_dashboard(request):
    return render(request, 'employer_dashboard.html')

def applicant_dashboard(request):
    return render(request, 'applicant_dashboard.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard')
def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting, Application
from .forms import JobPostingForm


@login_required
def employer_dashboard(request):
    job_postings = JobPosting.objects.filter(employer=request.user)
    context = {
        'job_postings': job_postings
    }
    return render(request, 'employer_dashboard.html', context)

@login_required
def add_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.employer = request.user
            job_posting.save()
            messages.success(request, 'Job posting added successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobPostingForm()
    return render(request, 'add_job_posting.html', {'form': form})

@login_required
def edit_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobPostingForm(instance=job_posting)
    return render(request, 'edit_job_posting.html', {'form': form})

@login_required
def delete_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    job_posting.delete()
    messages.success(request, 'Job posting deleted successfully!')
    return redirect('employer_dashboard')

def home(request):
    return render(request,'home.html')
@login_required
def applicant_dashboard(request):
    available_jobs = JobPosting.objects.filter(status='Open')
    applications = Application.objects.filter(applicant=request.user)
    
    context = {
        'available_jobs': available_jobs,
        'applications': applications,
    }
    return render(request, 'applicant_dashboard.html', context)

@login_required
def upload_resume(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job_posting = job_posting
            application.save()
            messages.success(request, 'Your resume and cover letter have been uploaded successfully!')
            return redirect('applicant_dashboard')
        else:
            messages.error(request, 'There was an error uploading your files. Please try again.')
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form, 'job_posting': job_posting})

from django.shortcuts import render, get_object_or_404
from .models import JobPosting, Application

def job_applications(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user)
    applications = Application.objects.filter(job_posting=job_posting)
    context = {
        'job_posting': job_posting,
        'applications': applications,
    }
    return render(request, 'job_applications.html', context)