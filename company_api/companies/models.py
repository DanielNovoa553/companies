import uuid
from django.db import models

class Company(models.Model):
    """ Modelo de compañía
    Args: models.Model: Modelo de Django
    Returns: models.Model: Modelo de compañía"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name
