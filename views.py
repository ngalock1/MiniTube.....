from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserProfileSerializer, UserPublicSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ - Create a new account."""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    """POST /api/auth/logout/ - Blacklist the refresh token."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    """GET/PUT /api/users/me/ - Own profile."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data,
            partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        return self.put(request)

class ChannelView(generics.RetrieveAPIView):
    """GET /api/auth/channel/<id>/ - Public channel page."""
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = (permissions.AllowAny,)
