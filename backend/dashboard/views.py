from django.contrib.auth import authenticate,login,logout
from rest_framework import generics, permissions,status
from .models import Indicator,User
from .serializers import IndicatorSerializer,RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

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
            return Response({'message':'username not found please register'},status = status.HTTP_404_NOT_FOUND)
        print('user is present')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print ("HIIII",request.user)
            
            return Response({'message':'login successful'},status= status.HTTP_200_OK)
        return Response({'message':'invalid credentials'},status = status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({'message':'logout sucessful'},status=status.HTTP_200_OK)

class IndicatorListView(generics.ListAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Indicator.objects.all().order_by("-year")
        year_min = self.request.query_params.get("year_min")
        year_max = self.request.query_params.get("year_max")
        indicator = self.request.query_params.get("indicator")

        if year_min:
            queryset = queryset.filter(year__gte=year_min)
        if year_max:
            queryset = queryset.filter(year__lte=year_max)
        if indicator:
            queryset = queryset.filter(indicator__icontains=indicator)

        return queryset

class FetchUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username
        })


class FetchWorldBankData(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        url = "http://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&per_page=60"
        r = requests.get(url)
        data = r.json()
        if len(data) < 2:
            return Response({"error": "Invalid World Bank API response"}, status=400)

        entries = data[1]
        for entry in entries:
            Indicator.objects.update_or_create(
                country=entry["country"]["value"],
                indicator=entry["indicator"]["value"],
                year=int(entry["date"]),
                defaults={"value": entry["value"]}
            )
        return Response({"message": "World Bank data fetched & saved"}, status=200)