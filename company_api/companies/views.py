import csv
import os
from uuid import UUID
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
import logging
from django.http import JsonResponse
from django.shortcuts import render
import json
import requests
from django.core.paginator import Paginator, EmptyPage

# Configuración del logger
logger = logging.getLogger(__name__)

# Clave de la API de Alpha Vantage
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Vista para listar y crear compañías
class CompanyListCreate(generics.ListCreateAPIView):
    """ Vista para listar y crear compañías
    Args: generics.ListCreateAPIView: Vista genérica de Django REST framework"""

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
    """ Vista para leer, actualizar y eliminar una compañía
    Args: generics.RetrieveUpdateDestroyAPIView: Vista genérica de Django REST framework"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# Vista para renderizar HTML
def companies_list_view(request):
    """ Vista para renderizar la lista de compañías
    Args: request (HttpRequest): La petición HTTP
    Returns: HttpResponse: La respuesta HTTP"""
    return render(request, 'companies/companies_list.html')

# Vista para renderizar el dashboard
def dashboard(request):
    """ Vista para renderizar el dashboard
    Args: request (HttpRequest): La petición HTTP
    Returns: HttpResponse: La respuesta HTTP"""
    return render(request, 'companies/dashboard.html')


def get_companies(request):
    """ Vista para obtener todas las compañías con paginación, búsqueda y ordenación.
    Args: request (HttpRequest): La petición HTTP
    Returns: JsonResponse: La respuesta JSON"""

    start = int(request.GET.get('start', 0))  # Índice del primer registro a mostrar
    length = int(request.GET.get('length', 10))  # Número de registros a mostrar
    search_value = request.GET.get('search[value]', '')  # Valor de búsqueda
    order_column = request.GET.get('order[0][column]', '0')  # Columna a ordenar
    order_dir = request.GET.get('order[0][dir]', 'asc')  # Dirección del orden (ascendente o descendente)

    # Definir las columnas para ordenar según el índice de las columnas de DataTable
    order_columns = ['id', 'name', 'description', 'symbol']

    # Filtrar los datos según el valor de búsqueda (si hay uno)
    if search_value:
        companies = Company.objects.filter(name__icontains=search_value)
    else:
        companies = Company.objects.all()

    # Ordenar los datos
    if order_column in ['0', '1', '2', '3']:  # Verifica que la columna exista
        order_field = order_columns[int(order_column)]
        if order_dir == 'desc':
            order_field = '-' + order_field
        companies = companies.order_by(order_field)

    # Contar el total de registros (antes de la paginación)
    total_records = companies.count()

    # Aplicar paginación manual
    companies_paginated = companies[start:start + length]

    # Serializar los datos
    serializer = CompanySerializer(companies_paginated, many=True)

    # Preparar la respuesta JSON con el formato {"companies": [...], "recordsTotal": x, "recordsFiltered": y}
    response = {
        'companies': serializer.data,        # Datos paginados y serializados
        'recordsTotal': total_records,       # Total de registros en la base de datos (antes de cualquier filtrado)
        'recordsFiltered': total_records     # Total de registros después del filtrado (iguales si no se usa búsqueda)
    }

    return JsonResponse(response, safe=False)


def get_company(request, id):
    """ Vista para obtener una compañía por ID
    Args: request (HttpRequest): La petición HTTP
          id (UUID): El ID de la compañía
      Returns: JsonResponse: La respuesta JSON
        Raises Company.DoesNotExist: Si la compañía no existe"""

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
    """ Vista para actualizar una compañía
    Args: request (HttpRequest): La petición HTTP
    Returns: JsonResponse: La respuesta JSON
    Raises ValueError: Si hay un error en los datos de la compañía"""
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
            if not symbol_exists:
                return JsonResponse({'error': 'Simbolo no es valido en la NYSE'}, status=400)

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
    """ Vista para agregar una nueva compañía
    Args: request (HttpRequest): La petición HTTP
    Returns: JsonResponse: La respuesta JSON
    Raises ValueError: Si hay un error en los datos de la compañía
    """
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

            if not symbol_exists:
                return JsonResponse({'error': 'El simbolo no es valido en la NYSE'}, status=400)

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
    """ Vista para eliminar una compañía
    Args: request (HttpRequest): La petición HTTP, id (UUID): El ID de la compañía
    Returns: JsonResponse: La respuesta JSON
    Raises Company.DoesNotExist: Si la compañía no existe"""

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


@csrf_exempt
def get_company_details(request, id):
    """ Vista para obtener los detalles de una compañía y los datos de mercado de los últimos 7 días
    Args:
        id (UUID): El ID de la compañía
    Returns: JsonResponse: Los detalles de la compañía y los datos de mercado
    """
    try:
        # Validar que el id sea un UUID válido
        try:
            UUID(str(id))
        except ValueError:
            return JsonResponse({'error': 'Invalid company_id format. Must be a valid UUID.'}, status=400)

        # Obtener los detalles de la compañía desde tu base de datos
        company = Company.objects.get(id=id)

        # Llamar a la API externa para obtener los datos de mercado de los últimos 7 días
        symbol = company.symbol  # El símbolo de la acción de la compañía
        market_data_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        response = requests.get(market_data_url)
        market_data = response.json()

        # Verificar si la respuesta contiene un mensaje de información
        if "Information" in market_data:
            return JsonResponse({'error': market_data["Information"]}, status=429)

        # Obtener los datos de los últimos 7 días
        last_7_days = list(market_data['Time Series (Daily)'].items())[:7]
        return JsonResponse({'company': last_7_days, 'companyName': company.name})
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
    except requests.RequestException as e:
        return JsonResponse({'error': f'Error fetching market data: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


