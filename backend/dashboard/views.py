# from django.contrib.auth import authenticate,login,logout
# from rest_framework import generics, permissions,status
# from .models import Indicator,User
# from .serializers import IndicatorSerializer,RegistrationSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# import requests

# #Create your views here.
# class RegistrationView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self,request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'Registration successful'},status = status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self,request):
#         username = request.data.get('username')
#         password = request.data.get('password')
        

#         if not User.objects.filter(username=username).exists():
#             return Response({'message':'username not found please register'},status = status.HTTP_404_NOT_FOUND)
#         print('user is present')
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             print ("HIIII",request.user)
            
#             return Response({'message':'login successful','user':{'username':'user.username','id':'user.id'}},status= status.HTTP_200_OK)
#         return Response({'message':'invalid credentials'},status = status.HTTP_401_UNAUTHORIZED)
    
# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self,request):
#         logout(request)
#         return Response({'message':'logout sucessful'},status=status.HTTP_200_OK)

# class IndicatorListView(generics.ListAPIView):
#     serializer_class = IndicatorSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = Indicator.objects.all().order_by("-year")
#         year_min = self.request.query_params.get("year_min")
#         year_max = self.request.query_params.get("year_max")
#         indicator = self.request.query_params.get("indicator")

#         if year_min:
#             queryset = queryset.filter(year__gte=year_min)
#         if year_max:
#             queryset = queryset.filter(year__lte=year_max)
#         if indicator:
#             queryset = queryset.filter(indicator__icontains=indicator)

#         return queryset

# class FetchUserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         print('used fetch user api')
#         user = request.user
#         return Response({
#             "id": user.id,
#             "username": user.username
#         })


# class FetchWorldBankData(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         url = "http://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&per_page=60"
#         r = requests.get(url)
#         data = r.json()
#         if len(data) < 2:
#             return Response({"error": "Invalid World Bank API response"}, status=400)

#         entries = data[1]
#         for entry in entries:
#             Indicator.objects.update_or_create(
#                 country=entry["country"]["value"],
#                 indicator=entry["indicator"]["value"],
#                 year=int(entry["date"]),
#                 defaults={"value": entry["value"]}
#             )
#         return Response({"message": "World Bank data fetched & saved"}, status=200)

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

from .forms import RegistrationForm,IndicatorForm
from .models import Indicator


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login-user")
        return render(request, "register.html", {"form": form})

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print('username',username)
        print('password',password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard-view")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login-user")



class DashboardView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        year = request.GET.get("year")
        country = request.GET.get("country")

        indicators = Indicator.objects.all().order_by("year")

        if year:
            indicators = indicators.filter(year=year)
        if country:
            indicators = indicators.filter(country__icontains=country)

        chart_data = [
            {"year": int(ind.year), "value": float(ind.value), "country": ind.country}
            for ind in indicators if ind.value is not None
        ]

       
        countries = Indicator.objects.values_list('country', flat=True).distinct().order_by('country')

        return render(request, "dashboard.html", {
            "chart_data": chart_data,
            "data_type": "population",
            "year": year,
            "country": country,
            "countries": countries,
        })



class IndicatorListView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        form = IndicatorForm()
        return render(request, "indicator_form.html", {"form": form})

    def post(self, request):
        form = IndicatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Indicator added successfully!")
            return redirect("dashboard")
        return render(request, "indicator_form.html", {"form": form})


class FetchWorldBankData(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        country = request.GET.get("country", "IN")
        indicator_code = request.GET.get("indicator", "SP.POP.TOTL")
        url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}?format=json"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                records = data[1]
                for rec in records:
                    if rec["value"] is not None:
                        Indicator.objects.update_or_create(
                            country=rec["country"]["value"],
                            indicator=rec["indicator"]["value"],
                            year=rec["date"],
                            defaults={"value": rec["value"]},
                        )
                messages.success(request, "World Bank data fetched successfully!")
        else:
            messages.error(request, "Failed to fetch data from World Bank API")

        return redirect("dashboard")

