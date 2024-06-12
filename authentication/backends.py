from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Essayez d'abord par e-mail
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Si l'utilisateur n'est pas trouvé par e-mail, essayez par numéro de téléphone
            try:
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return None

        # Vérifiez le mot de passe
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None