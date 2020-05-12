from django.db import models

# Create your models here.
class ElectricalCounter(models.Model):
    """Draft model for electrical counter."""
    class Meta:
         verbose_name = "счетчик эл.энергии"
         verbose_name_plural = "счетчики эл.энергии"

    def __str__(self):
         """String to represent the Model(class) object."""
         pass

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

