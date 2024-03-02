# Importing necessary modules and classes
from django.db import models  # Module for defining database models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # Base classes for custom user model

# Enumeration for user roles
class Roles(models.IntegerChoices):
    """
    Enumeration for user roles.

    Attributes:
        SUPER_USER: Integer representing a super user role with its display name in Persian.
        ADMIN: Integer representing an admin user role with its display name in Persian.
        USER: Integer representing a regular user role with its display name in Persian.
    """
    SUPER_USER = 1, "مدیرکل"
    ADMIN = 2, "مدیر"
    USER = 3, "کاربر عادی"

# Custom manager for the custom user model
class MyAccountManager(BaseUserManager):
    """
    Custom manager for the custom user model.

    This manager provides methods for creating regular users and superusers.
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Creates and saves a regular user with the given details.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user. Defaults to None.

        Raises:
            ValueError: If email or username is not provided.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """
        Creates and saves a superuser with the given details.

        Args:
            first_name (str): The first name of the superuser.
            last_name (str): The last name of the superuser.
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str): The password of the superuser.

        Returns:
            User: The created superuser object.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role = Roles.SUPER_USER
        user.save(using=self._db)

# Custom user model
class Account(AbstractBaseUser):
    """
    Custom user model.

    Attributes:
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        username (CharField): The username of the user.
        email (EmailField): The email address of the user.
        phone_number (CharField): The phone number of the user.
        date_joined (DateTimeField): The date and time when the user joined.
        last_login (DateTimeField): The date and time of the user's last login.
        is_admin (BooleanField): Flag indicating whether the user is an admin.
        is_staff (BooleanField): Flag indicating whether the user is staff.
        is_active (BooleanField): Flag indicating whether the user is active.
        is_superadmin (BooleanField): Flag indicating whether the user is a superadmin.
        role (IntegerField): The role of the user.
        object (MyAccountManager): The custom manager for the model.

    Methods:
        __str__(): Returns the string representation of the user.
        has_perm(): Checks if the user has a specific permission.
        has_module_perms(): Checks if the user has permissions for a specific module.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    role = models.IntegerField(choices=Roles.choices, default=Roles.USER)

    object = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """
        Returns the email address of the user.

        Returns:
            str: The email address of the user.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission.

        Args:
            perm (str): The permission to check.
            obj: Not used.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return self.is_admin

    def has_module_perms(self, add_label):
        """
        Checks if the user has permissions for a specific module.

        Args:
            add_label: Not used.

        Returns:
            bool: True if the user has permissions for the module, False otherwise.
        """
        return True
