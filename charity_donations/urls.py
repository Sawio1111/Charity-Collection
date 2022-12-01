"""charity_donations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from donations import views as donations

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', donations.LandingPageView.as_view(), name='main'),
    path('donation/', donations.AddDonationView.as_view(), name='add-donation'),
    path('login/', donations.LoginToView.as_view(), name='login'),
    path('logout/', donations.LogoutToView.as_view(), name='logout'),
    path('register/', donations.RegisterView.as_view(), name='register'),
    path('profile/', donations.UserProfileView.as_view(), name='profile'),
    path('form-confirmation/<str:info>/', donations.FormResponseView.as_view(), name='form-confirmation'),

    path('categories/', donations.ApiCategories.as_view(), name='api-categories'),
    path('form-request/', donations.ApiFormRequest.as_view(), name='form-request'),
    path('form-contact-request/', donations.ApiContactForm.as_view(), name='form-contact-request'),
]
