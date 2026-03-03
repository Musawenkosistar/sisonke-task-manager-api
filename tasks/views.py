from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable filter, search, ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    #  Filtering
    filterset_fields = ['completed']

    # Search
    search_fields = ['title', 'description']

    # Ordering
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Default order

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom Toggle Endpoint
    @action(detail=True, methods=['patch'])
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.completed = not task.completed
        task.save()

        return Response({
            "id": task.id,
            "completed": task.completed
        }, status=status.HTTP_200_OK)
