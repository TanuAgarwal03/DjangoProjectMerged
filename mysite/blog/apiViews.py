from rest_framework import viewsets , permissions ,generics,response
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
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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
    http_method_names = ['post','get','patch','delete']

class TagViewSet(viewsets.ModelViewSet):
    queryset =Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post','get','patch','delete']

class UserViewSet(viewsets.ModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get','patch','delete','post','put']  #requires modification

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

# class PasswordResetViewSet(viewsets.ViewSet):
#     # queryset = []
#     def forgot_password(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.filter(email=email).first()
#             if user:
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 token = default_token_generator.make_token(user)
#                 reset_url = reverse('password-reset-confirm')
#                 reset_url += f'?uid={uid}&token={token}'
#                 send_mail(
#                     'Password Reset Request',
#                     f'Please use the following link to reset your password: {reset_url}',
#                     'from@example.com',
#                     [email],
#                     fail_silently=False,
#                 )
#                 return Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def reset_password(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             new_password = serializer.validated_data['new_password']
#             user = User.objects.filter(email=email).first()
#             if user:
#                 user.set_password(new_password)
#                 user.save()
#                 return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse('password-reset-confirm') + f'?uid={uid}&token={token}'
            send_mail(
                'Password Reset Request',
                f'Please click the following link to reset your password: {reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return response.Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
        return response.Response({'detail': 'Email address not found.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        uid = request.query_params.get('uid')
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return response.Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        return response.Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


# class PasswordReset(generics.GenericAPIView):
#     serializer_class= EmailSerializer

#     def post(self ,request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # email = serializer.data("email")
#         email = serializer.validated_data["email"]
#         user =User.objects.filter(email=email).first()
#         if user:
#             encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
#             token = PasswordResetTokenGenerator().make_token(user)

#             # reset_url = reverse(
#             #     "reset-password" ,
#             #     kwargs={"encode_pk" :encoded_pk,"token" : token}
#             #     )
#             reset_url = reverse("reset-password", kwargs={"encoded_pk": encoded_pk, "token": token})

#             reset_url =f"http://127.0.0.1:8000/{reset_url}"

#             return response.Response(
#                 {
#                     "message":
#                     f"your password reset link: {reset_url}"
#                 },
#                 status = status.HTTP_200_OK,
#             )
#         else:
#             return response.Response(
#                 {"message": "User doesn't exists"},
#                 status =status.HTTP_400_BAD_REQUEST,
#             )
        
# class ResetPassword(generics.GenericAPIView):
#     serializer_class= ResetPasswordSerializer

#     def put(self, request,*args ,**kwargs):
#         serializer = self.serializer_class(
#             data=request.data ,context={"kwargs": kwargs}
#         )
#         serializer.is_valid(raise_exception=True)

#         return response.Response(
#             {"message":"Password reset successfully"},
#             status=status.HTTP_200_OK,
#         )