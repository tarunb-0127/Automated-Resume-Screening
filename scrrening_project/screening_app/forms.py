from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Application

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    company_name = forms.CharField(required=False)  # Optional initially

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'company_name', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        company_name = cleaned_data.get('company_name')

        if user_type == CustomUser.USER_TYPE_EMPLOYER and not company_name:
            self.add_error('company_name', 'Company name is required for employers.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.company_name = self.cleaned_data['company_name']
        if commit:
            user.save()
        return user

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    USER_TYPE_CHOICES = [
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    ]
    
    user_type = forms.MultipleChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

from .models import JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ('title', 'description', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})  # Example of adding a CSS class to the widget



class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError('The resume must be in PDF format.')
        return resume

    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        # Optionally add validation for the cover letter here
        return cover_letter