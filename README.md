# 📈 Django Companies API

Este proyecto es una API RESTful desarrollada en Django que permite **gestionar información de compañías**: crear, leer, actualizar, eliminar y consultar datos del mercado bursátil. Integra validaciones con un archivo CSV de símbolos de la **Bolsa de Nueva York (NYSE)** y se conecta a la **API de Alpha Vantage** para mostrar datos financieros.

---

## 🚀 Características

- CRUD completo para compañías (`name`, `description`, `symbol`).
- Validación contra un archivo CSV de símbolos NYSE.
- Dashboard HTML básico.
- Integración con la API de Alpha Vantage.
- Paginación, ordenamiento y búsqueda con DataTables.
- Validaciones personalizadas.
- Manejo de errores con logs.

---

## 🧱 Estructura del Proyecto
companies/ ├── views.py ├── models.py ├── serializers.py ├── templates/companies/ │ ├── companies_list.html │ └── dashboard.html └── nyse/nyse_symbols.csv


---

## ⚙️ Requisitos

- Python 3.7+
- Django
- Django REST Framework
- requests
- Archivo `.env` con:


---

## 📦 Instalación

1. Clona el repositorio:
 ```bash
 git clone https://github.com/tu-usuario/companies-api.git
 cd companies-api
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt

ALPHA_VANTAGE_API_KEY=TU_CLAVE

python manage.py migrate

python manage.py runserver

🧪 Endpoints Principales
Método	Ruta	Descripción
GET	/api/companies/	Lista todas las compañías
POST	/api/companies/	Crea una nueva compañía
GET	/api/companies/<id>/	Obtiene una compañía por ID
PUT	/api/companies/<id>/	Actualiza una compañía
DELETE	/api/companies/<id>/	Elimina una compañía
GET	/get-companies/	Lista paginada para DataTables
POST	/add-company/	Agrega una compañía (validando CSV)
POST	/update-company/<id>/	Actualiza una compañía (validando CSV)
DELETE	/delete-company/<id>/	Elimina una compañía
GET	/get-company-details/<id>/	Consulta de mercado (Alpha Vantage)

📊 Datos Financieros
Se utiliza Alpha Vantage para obtener datos de mercado de los últimos 7 días mediante el símbolo de la acción.

🧾 Validaciones
name: máximo 50 caracteres

description: máximo 100 caracteres

symbol: máximo 10 caracteres

El símbolo debe existir en el archivo nyse_symbols.csv

🪵 Logs
Los errores se registran mediante logging en el archivo configurado (por defecto, errors.log si así se configura en settings.py).

