from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions,status
from .models import Indicator,User
from .serializers import IndicatorSerializer,UserSerializer,RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Registration successful'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not User.objects.filter(username=username).exists():
            return Response({'error':'username not found please register'},status = status.HTTP_404_NOT_FOUND)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return Response({'message':'login successful'},status= status.HTTP_200_OK)
        return Response({'error':'invalid credentials'},status = status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({'message':'logout sucessful'},status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class IndicatorListCreateView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [permissions.IsAuthenticated]

class IndicatorDetailView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    