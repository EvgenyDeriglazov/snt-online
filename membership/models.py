from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from index.models import LandPlot

# Create your models here.
class MPayment(models.Model):
    """Represents membership payment."""
    payment_date = models.DateTimeField(
        "Дата оплаты",
        help_text="Фактическая дата оплаты",
        blank=True,
        )
    year_period = models.CharField(
        "Год",
        max_length=4,
        help_text="Членский взнос за определенный год",
        )

    month_period = models.CharField(
        "Месяц",
        help_text="Членский взнос за определенный месяц",
        )
    fee = models.DecimalField(
        "Размер взноса",
        help_text="Размер членского взноса за сотку (100 м.кв)",
        max_digits=7,
        decimal_places=2,
        )
    plot_area = models.PositiveIntegerField(
    	"Площадь участка",
    	help_text="Площадь участка в метрах квадратных",
    	)
    fee_amount = models.DecimalField(
    	"Сумма",
        help_text="Общая сумма к оплате",
        max_digits=7,
        decimal_places=2,
    	)
    land_plot = models.ForeignKey(
        LandPlot,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Номер участка",
        help_text="Номер участка",
    	)
   	STATUS = [
        ('n', 'Новые показания'),
        ('p', 'Оплачено'),
        ('c', 'Оплата подтверждена'),
    	] 
    status = models.CharField(
        "Статус",
        max_length=1,
        choices=STATUS,
        default='n',
        help_text="Статус квитанции",
    ) 
    class Meta:
        verbose_name = "членский взнос"
        verbose_name_plural = "членские взносы"

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.year_period + " " + self.land_plot.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass