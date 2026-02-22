from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_email_address(email: str):
    try:
        validate_email(value=email)
    except ValidationError:
        raise ValidationError("Enter a valid email address")


class UserManager(DjangoUserManager):

    def _create_user(
        self, username: str, email: str, password: str | None, **extra_fields
    ):

        # Check whether email and username is present or not
        if not username:
            raise ValueError(_("A username must be provided"))

        if not email:
            raise ValueError(_("An email address must be provided"))

        # Normalize and validate the email
        email = self.normalize_email(email=email)
        validate_email_address(email=email)

        global_user_model = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        print("Global User Model - ", global_user_model)
        print(type(global_user_model))

        username: str = global_user_model.normalize_username(username)

        user = self.model(username=username, email=email, **extra_fields)

        # Hash and assign the hashed password to user
        user.password = make_password(password=password)

        # Save the user
        user.save(using=self.db)

        return user

    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )

    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Additonal validations
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser True"))

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )
