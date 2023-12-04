from core.models import Note
from core.serializers import NoteSerializer
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

class NoteCreateList(ListCreateAPIView):
    permission_classes=[AllowAny]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes=[AllowAny]
    queryset=Note.objects.all()
    serializer_class = NoteSerializer
    