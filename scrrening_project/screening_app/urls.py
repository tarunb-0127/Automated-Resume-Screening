from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/add_job_posting/', views.add_job_posting, name='add_job_posting'),
    path('employer/edit_job_posting/<int:job_id>/', views.edit_job_posting, name='edit_job_posting'),
    path('employer/delete_job_posting/<int:job_id>/', views.delete_job_posting, name='delete_job_posting'),
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applicant/upload_resume/<int:job_id>/', views.upload_resume, name='upload_resume'),
    path('employer/job_applications/<int:job_id>/', views.job_applications, name='job_applications'),
    # other paths...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
