from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from .models import User, Role, Permission, AuditLog
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, AuditLogSerializer
from .forms import UserForm, RoleForm
from .utils import log_access_attempt


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        try:
            role = Role.objects.get(id=request.data['role_id'])
            user.roles.add(role)
            return Response({'status': 'role assigned'}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = UserForm()
    return render(request, 'rbac/create_user.html', {'form': form})

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role-list')
    else:
        form = RoleForm()
    return render(request, 'rbac/create_role.html', {'form': form})

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        try:
            role = Role.objects.get(id=request.data['role_id'])
            user.roles.add(role)
            log_access_attempt(request.user, "assign_role", f"Role: {role.name}", True)
            return Response({'status': 'role assigned'}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            log_access_attempt(request.user, "assign_role", "Invalid Role", False)
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    @action(detail=False, methods=['get'])
    def recent_logs(self, request):
        """To Get logs from the past 24 hours."""
        from django.utils.timezone import now, timedelta
        last_24_hours = now() - timedelta(hours=24)
        logs = AuditLog.objects.filter(timestamp__gte=last_24_hours)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
