# serializers.py

from rest_framework import serializers
from .models import RegisterUser, Permission, Module, UserPermission, UserModule
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from .models import RegisterUser
# from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import RegisterUser, Permission, Module, UserPermission, UserModule
from django.contrib.auth.models import Group

# Custom User Serializer
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'middle_name', 'phone',
            'department', 'role_level', 'account_type', 'role', 'active', 'status',
            'admin', 'store_id', 'location', 'unit', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = RegisterUser.objects.create_user(**validated_data)
        return user

# Custom Permission Serializer
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'content_type', 'name', 'codename']

# Module Serializer
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'app_name']

# User Serializer with Permissions and Modules
class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()

    class Meta:
        model = RegisterUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'middle_name', 'phone',
            'department', 'role_level', 'account_type', 'role', 'active', 'status',
            'admin', 'store_id', 'location', 'unit', 'permissions', 'modules'
        ]

    def get_permissions(self, obj):
        # Fetch permissions for the user from the custom UserPermission model
        permissions = UserPermission.objects.filter(user=obj)
        return PermissionSerializer([perm.permission for perm in permissions], many=True).data

    def get_modules(self, obj):
        # Fetch modules accessible by the user from the UserModule model
        modules = UserModule.objects.filter(user=obj)
        return ModuleSerializer([mod.module for mod in modules], many=True).data


# Group Serializer with Custom Permission Handling
class GroupSerializer(serializers.ModelSerializer):
    # Use custom Permission model instead of Django's default
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),  # Ensure it's your custom Permission model
        many=True
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        group = super().create(validated_data)
        
        # Link permissions with the group; adjust this if you have a custom logic
        for permission in permissions:
            # If you have a custom UserPermission or GroupPermission model, adjust here
            group.permissions.add(permission)
        
        return group

    def update(self, instance, validated_data):
        # Update permissions when modifying a group
        permissions = validated_data.pop('permissions', [])
        instance = super().update(instance, validated_data)
        
        # Adjust permissions for the group
        if permissions:
            instance.permissions.set(permissions)
        
        return instance
    

from rest_framework import serializers
from .models import Permission

class PermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']  # Only return 'id' and 'name'
