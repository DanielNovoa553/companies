import csv
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
import json

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

def get_company(request, id):
    try:
        company = Company.objects.get(id=id)
        data = {
            'id': company.id,
            'name': company.name,
            'description': company.description,
            'symbol': company.symbol
        }
        return JsonResponse(data)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)

@csrf_exempt
def update_company(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if len (data['name']) > 50:
              return JsonResponse({'error': 'Name cannot exceed 50 characters'}, status=400)
            if len (data['description']) > 100:
                return JsonResponse({'error': 'Description cannot exceed 100 characters'}, status=400)
            if len (data['symbol']) > 10:
                return JsonResponse({'error': 'Symbol cannot exceed 10 characters'}, status=400)

            symbol_exists = False
            csv_file_path = r'C:\Users\danie\PycharmProjects\companies\company_api\companies\nyse\nyse_symbols.csv'
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['Ticker'] == data['symbol']:
                        symbol_exists = True
                        break
            if symbol_exists:
                return JsonResponse({'error': 'Simbolo ya registrado en el NYSE'}, status=400)

            company = Company.objects.get(id=id)
            company.name = data['name']
            company.description = data['description']
            company.symbol = data['symbol']
            company.save()
            return JsonResponse({'message': 'Company updated successfully'})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def add_company(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if len(data['name']) > 50:
                return JsonResponse({'error': 'Name cannot exceed 50 characters'}, status=400)
            if len(data['description']) > 100:
                return JsonResponse({'error': 'Description cannot exceed 100 characters'}, status=400)
            if len(data['symbol']) > 10:
                return JsonResponse({'error': 'Symbol cannot exceed 10 characters'}, status=400)

            # Leer el archivo CSV y verificar el símbolo
            symbol_exists = False
            csv_file_path = r'C:\Users\danie\PycharmProjects\companies\company_api\companies\nyse\nyse_symbols.csv'
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['Ticker'] == data['symbol']:
                        symbol_exists = True
                        break

            if symbol_exists:
                return JsonResponse({'error': 'Simbolo ya registrado en el NYSE'}, status=400)

            company = Company(
                name=data['name'],
                description=data['description'],
                symbol=data['symbol']
            )
            company.save()
            return JsonResponse({'message': 'Company added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def delete_company(request, id):
    if request.method == 'DELETE':
        try:
            company = Company.objects.get(id=id)
            company.delete()
            return JsonResponse({'message': 'Company deleted successfully'})
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)