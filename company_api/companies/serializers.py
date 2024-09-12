import csv
from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'symbol']

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder los 50 caracteres.")
        return value

    def validate_description(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("La descripción no puede exceder los 100 caracteres.")
        return value

    def validate_symbol(self, value):
        # Validar el símbolo usando el archivo CSV
        if is_valid_symbol_in_csv(value):
            raise serializers.ValidationError("El símbolo no es válido o  está registrado en la NYSE.")
        return value


def is_valid_symbol_in_csv(symbol):
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
