from django.contrib.auth.models import UserManager
import django.dispatch


user_signal = django.dispatch.Signal()
    

class CitizenManager(UserManager):
    def _create_user(self, nin, password, **kwargs):
        if not nin or not password:
            raise ValueError("NIN and password must be set")
            
        user = self.model(nin=nin, **kwargs)
        user.save()
        return user

    def create_user(self, nin, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        
        return self._create_user(nin, password, **kwargs)

    def create_superuser(self, nin, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(nin, password, **kwargs)