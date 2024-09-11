from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_APPLICANT = 'applicant'
    USER_TYPE_EMPLOYER = 'employer'
    
    USER_TYPE_CHOICES = [
        (USER_TYPE_APPLICANT, 'Applicant'),
        (USER_TYPE_EMPLOYER, 'Employer'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Add company_name field
    
    def __str__(self):
        return self.username

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')])
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_postings')
    
    def __str__(self):
        return self.title

class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    date_applied = models.DateField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Add this line as nullable
    
    def __str__(self):
        return f"Application for {self.job_posting.title} by {self.applicant.username}"

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    date_sent = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
