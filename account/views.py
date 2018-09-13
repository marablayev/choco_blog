from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from .serializers import AuthorSerializer
from .models import Author

class AuthViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        author.set_password(data['password'])
        author.save()

        payload = jwt_payload_handler(author)
        token = jwt_encode_handler(payload)
        return Response({'token': token})
