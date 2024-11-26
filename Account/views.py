from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Module, UserPermission
from .serializers import ModuleSerializer, PermissionListSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from .serializers import GroupSerializer
from rest_framework import generics
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from rest_framework import generics
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from .models import Module, Permission, RegisterUser
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import GroupSerializer, PermissionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import RegisterUser, UserPermission
from .serializers import UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
       
        return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ModuleViewSet(viewsets.ModelViewSet):
    """
    View to manage Modules.
    Only accessible by admin users.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    # permission_classes = [IsAdminUser]  # Only admins can manage modules

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        app_name = data.get('app_name')
        content_type_id = data.get('content_type_id')
        group_ids = data.get('group_ids', [])

        try:
            content_type = ContentType.objects.get(id=content_type_id)
            module = Module.objects.create(
                name=name,
                app_name=app_name,
                content_type=content_type
            )

            # Assign the module to groups
            groups = Group.objects.filter(id__in=group_ids)
            module.group.set(groups)
            module.save()

            serializer = self.get_serializer(module)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid content type ID'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        module = self.get_object()
        data = request.data

        # Update fields
        module.name = data.get('name', module.name)
        module.app_name = data.get('app_name', module.app_name)

        # Update related groups
        group_ids = data.get('group_ids', [])
        groups = Group.objects.filter(id__in=group_ids)
        module.group.set(groups)

        module.save()
        serializer = self.get_serializer(module)
        return Response(serializer.data)


class GroupCreateAPIView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        group_name = data.get('name')
        permission_ids = data.get('permission_ids',[])
        # from django.contrib.auth.models import Permission
        # permissions = Permission.objects.all()
        # print(permissions)

        print("permission:",permission_ids)

        # Create or retrieve the group
        group, created = Group.objects.get_or_create(name=group_name)

        print("group:", group)

        # Assign permissions to the group
        permissions = Permission.objects.filter(id__in=permission_ids)
        print("permission:", permissions)
        group.permissions.set(permissions)

        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if RegisterUser.objects.filter(email=email).exists():
            return Response({'success': False, 'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = RegisterUser.objects.create_user(
            email=email,
            password=password,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            middle_name=data.get('middle_name'),
            phone=data.get('phone'),
            department=data.get('department'),
            role_level=data.get('role_level'),
            account_type=data.get('account_type'),
            role=data.get('role')
        )

        # Optionally assign a group to the user
        group_name = data.get('role')
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        # Assign any default permissions associated with the group to the user
        permissions = group.permissions.all()
        for perm in permissions:
            user.user_permissions.add(perm)

        serializer = UserSerializer(user)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
    

# UserPermission View for managing custom user-specific permissions
class UserPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            permissions = user.custom_user_permissions.all()  # Fetching using custom relation
            data = [{'name': perm.permission.name, 'codename': perm.permission.codename} for perm in permissions]
            return Response({'permissions': data})
        except RegisterUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            permission = request.data.get('permission', [])

            # Assign custom permissions to the user using UserPermission
            permissions = Permission.objects.filter(id__in=permission)
            UserPermission.objects.filter(user=user).delete()  # Clear existing permissions

            # Assign new permissions
            for permission in permissions:
                UserPermission.objects.create(user=user, permission=permission)

            serializer = UserSerializer(user)
            return Response(serializer.data)
        except RegisterUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



# from .serializers import PermissionSerializer

class PermissionListAPIView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer

