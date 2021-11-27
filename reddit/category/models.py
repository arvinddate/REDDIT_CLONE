from django.db import models

# Create your models here.
class Category(models.Model):
     
    title=models.CharField(max_length=255)
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

