from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse

from .backends import EmailOrPhoneModelBackend

from . import forms
from . import models

# from orders.models import Order

# Create your views here.


class ChangePasswordView(PasswordChangeView):
    template_name = 'authentication/account/change_password_form.html'
    #success_url = reverse_lazy('acount_change_password')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Mot de passe changé avec succès.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'change_password'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Mot de passe changé avec succès.')
        return reverse('account_change_password') 


class Login(View):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'
    success = False
    
    def get(self, request):
        form = self.form_class()
        message = ''
        
        return render(request, self.template_name, { 'form': form, 'success': self.success, 'message' : message }) 
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            backend = EmailOrPhoneModelBackend()
            user = backend.authenticate(
                request=request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            if user is not None:
                login(request, user)
                # message = f'Hello { user.username } ! You\'re logged in'
                # self.success = True
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Identifiant/password invalid"
        return render(request, self.template_name, { 'form': form, 'success': self.success, 'message' : message }) 
        


def signin(request):
    form = forms.LoginForm()
    
    message_error = ''
    success = False
    
    if request.method == 'POST':
        
        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            backend = EmailOrPhoneModelBackend()
            user = backend.authenticate(
                request=request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            if user is not None:
                # login(request, user)
                login(request, user, backend='authentication.backends.EmailOrPhoneModelBackend')
                # message = f'Hello { user.username } ! You\'re logged in'
                # success = True
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message_error = "Identifiant ou mot de passe incorrect"
        else:
            message_error = "Identifiant ou mot de passe incorrect"
            
    
    template_name = 'authentication/login.html'
    context = {
        'form': form, 
        'success': success, 
        'message_error' : message_error 
    }
        
    return render(request, template_name, context=context)


# def log_out(request):
    
#     logout(request)
#     return redirect('login')


def register(request):
    template_name = 'authentication/register.html'
    form = forms.RegisterForm()
    
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        
    return render(request, template_name, { 'form': form})



@login_required
def profile(request):
    
    
    template_name = "authentication/account/profile.html"
    page = "account_info"
    context = {
        'page': page
    }
    
    return render(request, template_name, context=context)


@login_required
def change_identifiants(request):
    
    if request.method == 'POST':
        form = forms.EditUserIdForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Informations mises à jour avec succès.')
            return redirect('account_change_identifiants')
    else:
        form = forms.EditUserIdForm(instance=request.user)
        
    template_name = "authentication/account/change_identifiants.html"
    page = "change_identifiants"
    context = {
        'page': page,
        'form': form,
    }

    return render(request, template_name, context=context)




@login_required
def addresses(request):
    
    addresses = models.Address.objects.all()
    
    template_name = "authentication/account/addresses.html"
    page = "address"
    context = {
        'page': page,
        'addresses': addresses,
    }
    
    return render(request, template_name, context=context)


@login_required
def addresses_create(request):
    
    form = forms.AddressForm()
    
    if request.method == 'POST':
        form = forms.AddressForm(request.POST)
        
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            return redirect('account_addresses')
    
    template_name = "authentication/account/addresses_create.html"
    page = "address"
    context = {
        'page': page,
        'form': form,
    }
    
    return render(request, template_name, context=context)


# @login_required
# def orders(request):
#     template_name = 'authentication/account/orders.html'
#     page = "orders"
    
#     orders = Order.objects.all().order_by('-created_at')
#     orders_complete = Order.objects.filter(is_paid=True).order_by('-created_at')
#     orders_in_progress = Order.objects.filter(is_paid=False).order_by('-created_at')
    
#     context = {
#         'page': page,
#         'orders': orders,
#         'orders_complete': orders_complete,
#         'orders_in_progress': orders_in_progress,
#     }
    
#     return render(request, template_name, context=context)