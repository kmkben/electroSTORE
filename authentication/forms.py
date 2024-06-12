from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
import phonenumbers
from django.core.exceptions import ValidationError

from . import models

class LoginForm(forms.Form):
    username = forms.fields.CharField(
        required=True, max_length=63, 
        label='Numéro de téléphone ou adresse email',
        error_messages={'required': 'Veuillez renseigner un identifiant (Numéro de téléphone ou adresse email) .'}
    )
    password = forms.fields.CharField(
        required=True, max_length=63, 
        widget=forms.PasswordInput, 
        label='Mot de passe',
        error_messages={'required': 'Veuillez renseigner un mot de passe.'}
    )
    
    
    
class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(
        required=True, 
        max_length=30, 
        label='Prénom',
        error_messages={'required': 'Veuillez renseigner votre prénom.'}
    )
    last_name = forms.CharField(
        required=True, 
        max_length=30, 
        label='Nom de famille',
        error_messages={'required': 'Veuillez renseigner votre nom de famille.'}
    )
    email = forms.EmailField(
        required=True, 
        max_length=254, 
        label='Adresse email',
        error_messages={'required': 'Veuillez renseigner votre adresse email.'}
    )
    phone = forms.CharField(
        required=True, 
        max_length=20, 
        label='Numéro de téléphone',
        error_messages={'required': 'Veuillez renseigner votre numéro de téléphone.'}
    )
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'email']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].validators.append(self.validate_phone_number)
        
    def validate_phone_number(self, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Veuillez entrer un numéro de téléphone valide.")
        except phonenumbers.NumberParseException:
            raise ValidationError("Veuillez entrer un numéro de téléphone valide")
        
        
        

class EditUserIdForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()  
        fields = ['email', 'phone']  # Add other fields as needed
        
        
        
class AddressForm(forms.ModelForm):
    name = forms.CharField(
        required=True, 
        max_length=128, 
        label='Nom de l\'adresse',
        error_messages={'required': 'Veuillez renseigner un pour votre adresse.'}
    )
    
    fullname = forms.CharField(
        required=True, 
        max_length=255, 
        label='Votre nom complet',
        error_messages={'required': 'Veuillez renseigner votre prénom et votre nom .'}
    )
    
    company = forms.CharField(
        required=False, 
        max_length=30, 
        label='Société'
    )
    
    address = forms.CharField(
        required=True, 
        label='Adresse',
        error_messages={'required': 'Veuillez renseigner votre adresse.'}
    )
    
    addressComplement = forms.CharField(
        required=False, 
        max_length=255, 
        label='Complément d\'adresse'
    )
    
    zip = forms.CharField(
        required=True, 
        max_length=10, 
        label='Code postal',
        error_messages={'required': 'Veuillez renseigner votre code postal.'}
    )
    
    city = forms.CharField(
        required=True, 
        max_length=64, 
        label='Ville ou commune',
        error_messages={'required': 'Veuillez renseigner votre ville ou commune.'}
    )
    
    country = forms.CharField(
        required=True, 
        max_length=64, 
        label='Pays',
        error_messages={'required': 'Veuillez renseigner votre pays.'}
    )
    
    phone = forms.CharField(
        required=True, 
        max_length=20, 
        label='Numéro de téléphone',
        error_messages={'required': 'Veuillez renseigner votre numéro de téléphone.'}
    )
    
    
    class Meta:
        model = models.Address
        fields = ['name', 'company', 'fullname', 'address', 'addressComplement', 'zip', 'city', 'country', 'phone']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs = {'rows': 4}
        self.fields['phone'].validators.append(self.validate_phone_number)
        
        
    def validate_phone_number(self, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Veuillez entrer un numéro de téléphone valide.")
        except phonenumbers.NumberParseException:
            raise ValidationError("Veuillez entrer un numéro de téléphone valide")