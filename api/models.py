from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.

class Book(models.Model):
    name=models.CharField(max_length=100)    # book name
    isbn_no=models.IntegerField(
        validators=[MaxValueValidator(9999999999999)] # 13 digits max
    )
    author_name=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    inventory=models.IntegerField()
    publication_year=models.PositiveIntegerField()

    