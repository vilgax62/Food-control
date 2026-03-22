from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from.serializer import NGOSerializer
from.models import NGOProfile

class NGOProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NGOSerializer
    
    def get_queryset(self):
        return NGOProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    