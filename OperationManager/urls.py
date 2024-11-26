"""
URL configuration for OperationManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from Account.views import  PermissionListAPIView, UserPermissionView
from Account.views import GroupCreateAPIView, GroupListAPIView, GroupRetrieveUpdateDestroyAPIView, LoginView, ModuleViewSet, RegisterView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'modules', ModuleViewSet, basename='module')





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Integrate dj-rest-auth URLs
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/user-permissions/<int:user_id>/', UserPermissionView.as_view(), name='user-permissions'),
    path('groups/', GroupListAPIView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateAPIView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group-detail'),
    path('permissions/', PermissionListAPIView.as_view(), name='permission-list'),
]

