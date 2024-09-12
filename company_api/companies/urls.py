from django.urls import path
from .views import CompanyListCreate, CompanyDetail, TestErrorView, companies_list_view, company_data_view, update_company, add_company, delete_company
from . import views


urlpatterns = [
    path('companies/', companies_list_view, name='companies-list'),  # Vista para renderizar el HTML
    path('companies/api/', CompanyListCreate.as_view(), name='company-list-create'),  # Listar y crear compañías (API)
    path('companies/<uuid:pk>/', CompanyDetail.as_view(), name='company-detail'),  # Leer, actualizar y eliminar compañías (API)
    path('test-error/', TestErrorView.as_view(), name='test-error'),  # Vista para probar el logging
    path('get_companies/', company_data_view, name='get-companies'),
    path('get_company/<uuid:id>/', views.get_company, name='get_company'),
    path('update_company/<uuid:id>/', update_company, name='update_company'),
    path('add_company/', add_company, name='add_company'),
    path('delete_company/<uuid:id>/', delete_company, name='delete_company'),
]


