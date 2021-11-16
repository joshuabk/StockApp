from django.db import models

# Create your models here.
class stock(models.Model):
    symbol = models.CharField(max_length = 6, default = "F")
    def __str__ (self):
        return self.ticker
 