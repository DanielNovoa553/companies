import csv
import requests
import uuid

# URL de la API para registrar empresas
api_url = 'http://localhost:8000/add_company/'  # Cambia esto a la URL correcta de tu API

# Función para obtener el token CSRF
def get_csrf_token():
    # Aquí debes implementar la lógica para obtener el token CSRF si es necesario
    return 'tu_token_csrf'

# Ruta del archivo CSV
csv_path = r'C:\Users\danie\PycharmProjects\companies\company_api\companies\nyse\nyse_symbols.csv'  # Cambia esto a la ruta correcta de tu archivo CSV

# Leer el archivo CSV
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        symbol, name, market = row
        # Generar un UUID-4 para la empresa
        company_id = str(uuid.uuid4())
        # Crear el payload para la solicitud POST
        payload = {
            'id': company_id,
            'name': name,
            'description': market,
            'symbol': symbol
        }
        # Enviar la solicitud POST
        response = requests.post(api_url, json=payload, headers={'X-CSRFToken': get_csrf_token()})
        if response.status_code == 200:
            print(f'Empresa {name} registrada correctamente con ID {company_id}.')
        else:
            print(f'Error al registrar la empresa {name}: {response.text}')