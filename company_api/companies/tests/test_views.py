
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from company_api.companies.models import Company
from uuid import uuid4
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.django_db
def test_get_company():
    client = APIClient()

    # Crear una instancia de Company para la prueba
    company = Company.objects.create(
        id=uuid4(),
        name="Test Company",
        description="Test Description",
        symbol="TEST"
    )

    # Probar que la función devuelve la compañía correcta
    url = reverse('get_company', args=[company.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        'id': str(company.id),
        'name': company.name,
        'description': company.description,
        'symbol': company.symbol
    }

    # Probar que la función devuelve un error para un ID no existente
    non_existent_id = uuid4()
    url = reverse('get_company', args=[non_existent_id])
    response = client.get(url)
    assert response.status_code == 404
    assert response.json() == {'error': 'Company not found'}
