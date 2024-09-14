import csv
from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """ Serializador para el modelo Company generico de Django REST
    Args: serializers.ModelSerializer: Serializador de Django REST
    Methods: validate_name, validate_description, validate_symbol

     """
    class Meta:
        """ Metaclase para el serializador CompanySerializer
        """
        model = Company
        fields = ['id', 'name', 'description', 'symbol']

    def validate_name(self, value):
        """ Validar el nombre de la compañía
        Args: value (str): El nombre de la compañía
        Returns: str: El nombre de la compañía validado
        Raises: serializers.ValidationError: Si el nombre excede los 50 caracteres"""
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder los 50 caracteres.")
        return value

    def validate_description(self, value):
        """ Validar la descripción de la compañía
        Args: value (str): La descripción de la compañía
        Returns: str: La descripción de la compañía validada
        Raises: serializers.ValidationError: Si la descripción excede los 100 caracteres"""
        if len(value) > 100:
            raise serializers.ValidationError("La descripción no puede exceder los 100 caracteres.")
        return value

    def validate_symbol(self, value):
        """ Validar el símbolo de la compañía
        Args: value (str): El símbolo de la compañía
        Returns: str: El símbolo de la compañía validado"""
        # Validar el símbolo usando el archivo CSV
        if is_valid_symbol_in_csv(value):
            raise serializers.ValidationError("El símbolo no es válido o  está registrado en la NYSE.")
        return value


def is_valid_symbol_in_csv(symbol):
    """ Verificar si un símbolo es válido en la NYSE
    Args: symbol (str): El símbolo a verificar
    Returns: bool: True si el símbolo es válido, False si no lo es"""
    # Ruta al archivo CSV con los símbolos válidos
    csv_file_path = r'C:\Users\danie\PycharmProjects\companies\company_api\companies\nyse\nyse_symbols.csv'
    # Abre y lee el archivo CSV
    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['Ticker'] == symbol:
                    return True
    except FileNotFoundError:
        raise serializers.ValidationError("Archivo CSV no encontrado. No se puede validar el símbolo.")

    return False  # Si no se encuentra el símbolo en el CSV, retorna False
