from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.
    """

    id = models.CharField(
        max_length=64, default=uuid4, primary_key=True, editable=False
    )
    created = models.DateTimeField("Data Criação", auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(
        "Data Atualização", auto_now=True, auto_now_add=False
    )

    class Meta:
        abstract = True
