from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render

# Configuración del logger
logger = logging.getLogger(__name__)

# Vista para listar y crear compañías
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error al crear la compañía: {str(e)}")
            raise e

# Vista para leer, actualizar y eliminar una compañía
class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class TestErrorView(View):
    def get(self, request):
        try:
            # Genera un error para probar el logging
            raise ValueError("Este es un error de prueba para logging")
        except Exception as e:
            # Registra el error
            logger.error("Error en TestErrorView: %s", str(e))
            return HttpResponse("Error registrado en logs.", status=500)

# Vista para renderizar HTML
def companies_list_view(request):
    return render(request, 'companies/companies_list.html')

def company_data_view(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return JsonResponse({"companies": serializer.data}, safe=False)