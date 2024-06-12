"""
URL configuration for electroStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView

from . import views
import authentication.views

urlpatterns = [
    path('', views.home, name='home'),
    
    
    path('login/', authentication.views.signin, name='login'),
    path('register/', authentication.views.register, name='register'),
    path('logout/', LogoutView.as_view(
            next_page=None
        ), name='logout'),
    
    # path('account/change-password/', PasswordChangeView.as_view(
    #         template_name='authentication/account/change_password_form.html'),
    #         name='account_change_password',
    #         kwargs={'extra_context': {'page': 'change_password'}}
    #     ),
    path('account/change-password/', authentication.views.ChangePasswordView.as_view(), name='account_change_password'),
    path('account/change-password-done/', PasswordChangeDoneView.as_view(
            template_name='authentication/profile/change_password_done.html'),
            name='acount_change_password_done'
        ),
    
    path('account/', authentication.views.profile, name='account'),
    path('account/addresses', authentication.views.addresses, name='account_addresses'),
    path('account/addresses/create', authentication.views.addresses_create, name='account_addresses_create'),
    path('account/change-identifiants', authentication.views.change_identifiants, name='account_change_identifiants'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)