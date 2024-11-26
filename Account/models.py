# # models.py

# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
# from django.contrib.contenttypes.models import ContentType

# # Custom User model
# class RegisterUser(AbstractUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50, null=True, blank=True)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     department = models.CharField(max_length=100, null=True, blank=True)
#     role_level = models.CharField(max_length=10)
#     account_type = models.CharField(max_length=10)
#     role = models.CharField(max_length=10)
#     active = models.BooleanField(default=True)
#     status = models.CharField(max_length=10)
#     admin = models.BooleanField(default=False)
#     store_id = models.CharField(max_length=20, null=True, blank=True)
#     location = models.CharField(max_length=100, null=True, blank=True)
#     unit = models.CharField(max_length=100, null=True, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self):
#         return self.email


# # Permission Model
# class Permission(models.Model):
#     name = models.CharField(max_length=100)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="account_permission_set")  # Permissions are tied to models
#     codename = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.content_type}: {self.name}"


# # User Permissions Relationship
# class UserPermission(models.Model):
#     user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='user_permissions')
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.email} - {self.permission.name}"


# # Module Model
# class Module(models.Model):
#     name = models.CharField(max_length=255)
#     app_name = models.CharField(max_length=255)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Tie to specific models in the app
#     group = models.ManyToManyField(Group, related_name='modules')  # Roles related to this module

#     def __str__(self):
#         return self.name


# # User's accessible modules
# class UserModule(models.Model):
#     user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='user_modules')
#     module = models.ForeignKey(Module, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.email} - {self.module.name}"

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.contrib.contenttypes.models import ContentType

# Custom User model
class RegisterUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    role_level = models.CharField(max_length=10)
    account_type = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=10)
    admin = models.BooleanField(default=False)
    store_id = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


# Permission Model
class Permission(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="account_permission_set")  # Permissions are tied to models
    codename = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.content_type}: {self.name}"


# User Permissions Relationship
class UserPermission(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='custom_user_permissions')  # Changed related_name here
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.permission.name}"


# Module Model
class Module(models.Model):
    name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Tie to specific models in the app
    group = models.ManyToManyField(Group, related_name='modules')  # Roles related to this module

    def __str__(self):
        return self.name


# User's accessible modules
class UserModule(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='user_modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.module.name}"
