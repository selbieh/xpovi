from django.db import models




class BaseModel(models.Model):
    """
    Base model which contains global attributes and methods.
    """

    class Meta:
        abstract = True

    added_at = models.DateTimeField("Added at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True, null=True)