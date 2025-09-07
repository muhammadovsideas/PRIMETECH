from rest_framework import generics, permissions
from .serializers import *
from .models import *
from .permissions import IsAdmin,IsUser
from rest_framework.parsers import MultiPartParser, FormParser

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user