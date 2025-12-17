# api/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Conflict
from .serializers import ConflictSerializer

class ConflictViewSet(viewsets.ModelViewSet):
    queryset = Conflict.objects.all()
    serializer_class = ConflictSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        resolved = self.request.query_params.get('resolved', None)
        
        if resolved == 'true':
            queryset = queryset.filter(resolved=True)
        elif resolved == 'false':
            queryset = queryset.filter(resolved=False)
        
        return queryset
    
    def resolve(self, request, pk=None):
        conflict = self.get_object()
        conflict.resolved = True
        conflict.resolved_by = request.user
        conflict.resolved_at = timezone.now()
        conflict.resolution_notes = request.data.get('notes', '')
        conflict.save()
        
        return Response({'status': 'تم حل التعارض'})