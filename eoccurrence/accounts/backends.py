from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .models import Userprofile

UserModel = get_user_model()

class UsernameOrIdNumberBackend(ModelBackend):
    """
    Authenticate with either username or id_number from UserProfile.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Try username first
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Try ID number from profile
            try:
                profile = Userprofile.objects.get(id_number=username)
                user = profile.user
            except Userprofile.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
