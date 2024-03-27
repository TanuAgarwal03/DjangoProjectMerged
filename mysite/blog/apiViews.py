from rest_framework import viewsets , permissions
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password


class PostViewSet(viewsets.ModelViewSet):
    queryset= Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_field = ['created_date']
    http_method_names =['get' , 'post' ,'patch']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset =Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset =Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self , request, *args , **kwargs):
        user =request.user
        serializer = UserSerializer(user)
        return Response(serializer.data , status= status.HTTP_200_OK)
    
class PostCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Assuming you're using authentication
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewSet(viewsets.ModelViewSet):
    queryset = []
    http_method_names=['post']
    serializer_class = LoginSerializer

class UserSignViewSet(viewsets.ModelViewSet):
    queryset = []
    http_method_names = ['post']
    serializer_class = UserSerializer

class ChangePasswordViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        print(request)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            user = request.user

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been successfully updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]   
    http_method_names = ['post','get','patch']
