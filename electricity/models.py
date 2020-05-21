from django.db import models
from index.models import Snt, LandPlot

# Create your models here.
class ECounter(models.Model):
    """Draft model for electrical counter."""
    reg_date = models.DateField(
        "Дата регистрации",
        help_text="Укажите дату установки нового счетчика"
        + " или приемки к учету в веб приложении уже имеющегося",
        )
    model_name = models.CharField(
        "Название модели",
        max_length=100,
        help_text="Укажите название модели счетчика"
        )
    sn = models.CharField(
        "Серийный номер",
        max_length=50,
        help_text="Укажите серийный номер счетчика",
        )
    MODEL_TYPE_CHOICES = [
        ('single', 'Однотарифный'),
        ('double', 'Двухтарифный'),
        ]
    model_type = models.CharField(
        "Тип",
        max_length=6,
        help_text="Выберите тип счетчика",
        choices=MODEL_TYPE_CHOICES,
        )
    s = models.PositiveIntegerField(
        "Однотарифный",
        help_text="Показания счетчика на момент установки"
        + "/приемки к учету в веб приложении",
        blank=True,
        null=True,
        )
    t1 = models.PositiveIntegerField(
        "День",
        help_text="Показания счетчика (тариф день/Т1)"
        + " на момент установки/приемки к учету в веб приложении",
        blank=True,
        null=True,
        )
    t2 = models.PositiveIntegerField(
        "Ночь",
        help_text="Показания счетчика (тариф ночь/Т2)"
        + " на момент установки/приемки к учету в веб приложении",
        blank=True,
        null=True,
        )
    land_plot = models.OneToOneField(
        LandPlot,
        verbose_name="Участок",
        help_text="Выберите участок",
        on_delete=models.SET_NULL,
        null=True,
        )

    class Meta:
         verbose_name = "счетчик эл.энергии"
         verbose_name_plural = "счетчики эл.энергии"

    def __str__(self):
         """String to represent the Model(class) object."""
         return self.model_name

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

