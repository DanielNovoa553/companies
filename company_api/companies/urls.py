from django.urls import path
from .views import CompanyListCreate, CompanyDetail, companies_list_view, company_data_view, update_company, add_company, delete_company, get_company_details
from . import views

# URLs de la aplicación companies
urlpatterns = [
    path('companies/', companies_list_view, name='companies-list'),  # Vista para renderizar el HTML
    path('companies/api/', CompanyListCreate.as_view(), name='company-list-create'),  # Listar y crear compañías (API)
    path('companies/<uuid:pk>/', CompanyDetail.as_view(), name='company-detail'),  # Leer, actualizar y eliminar compañías (API)
    path('get_companies/', company_data_view, name='get-companies'), # Obtener todas las compañías (API)
    path('get_company/<uuid:id>/', views.get_company, name='get_company'), # Obtener una compañía (API)
    path('update_company/<uuid:id>/', update_company, name='update_company'), # Actualizar una compañía (API)
    path('add_company/', add_company, name='add_company'), # Añadir una compañía (API)
    path('delete_company/<uuid:id>/', delete_company, name='delete_company'), # Eliminar una compañía (API)
    path('get_company_details/<uuid:id>/', get_company_details, name='get_company_details'), # Obtener los detalles de una compañía (API)
]


