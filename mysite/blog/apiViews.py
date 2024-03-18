from rest_framework import viewsets , permissions
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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