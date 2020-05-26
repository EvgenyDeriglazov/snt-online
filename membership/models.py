from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from index.models import LandPlot, Snt
from membership.validators import *

# Create your models here.
class MPayment(models.Model):
    """Represents membership payment with detailed information about
    date, period, amount, landplot. Contains custom model methods."""
    payment_date = models.DateField(
        "Дата оплаты",
        help_text="Фактическая дата оплаты",
        blank=True,
        null=True,
        )
    year_period = models.CharField(
        "Год",
        max_length=4,
        help_text="Укажите год в виде 4-х значного числа",
        validators=[validate_number, validate_year_period_min_length],
        )
    MONTH_PERIOD_CHOICES = [
        ('', ''),
        ('Jan', 'Январь'),
        ('Feb', 'Февраль'),
        ('Mar', 'Март'),
        ('Apr', 'Апрель'),
        ('May', 'Май'),
        ('Jun', 'Июнь'),
        ('Jul', 'Июль'),
        ('Aug', 'Август'),
        ('Sep', 'Сентябрь'),
        ('Oct', 'Октябрь'),
        ('Nov', 'Ноябрь'),
        ('Dec', 'Декабрь'),
        ]
    month_period = models.CharField(
        "Месяц",
        help_text="Выберите месяц, если начисления" 
        + " членских взносов расчитываются помесячно",
        max_length=3,
        blank=True,
        choices=MONTH_PERIOD_CHOICES,
        default='',
        )
    rate = models.DecimalField(
        "Размер взноса",
        help_text="Размер членского взноса за сотку (100 м.кв)/рублей",
        max_digits=7,
        decimal_places=2,
        )
    plot_area = models.PositiveIntegerField(
        "Площадь участка",
        help_text="Площадь участка в квадратных метрах",
        )
    amount = models.DecimalField(
        "Сумма",
        help_text="Сумма взноса к оплате",
        max_digits=7,
        decimal_places=2,
        )
    land_plot = models.ForeignKey(
        LandPlot,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Участок",
        help_text="Выберите участок",
        )
    STATUS_CHOICES = [
        ('n', 'Неоплачено'),
        ('p', 'Оплачено'),
        ('c', 'Оплата подтверждена'),
        ] 
    status = models.CharField(
        "Статус",
        max_length=1,
        choices=STATUS_CHOICES,
        default='n',
        help_text="Статус оплаты",
    ) 
    class Meta:
        verbose_name = "членский взнос"
        verbose_name_plural = "членские взносы"
        constraints = [
            models.UniqueConstraint(
                fields=['year_period', 'month_period'],
                name='%(app_label)s_%(class)s_year_month_period',
                )
            ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.year_period + " " + self.land_plot.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass

class MRate(models.Model):
    """Represents membership payment rate for specific period of time."""
    date = models.DateField(
        "Дата",
        help_text="Укажите дату ввода тарифа",
        )
    year_period = models.CharField(
        "Год",
        max_length=4,
        help_text="Укажите год периода для произведения расчета" 
        + " в виде 4-х значного числа",
        validators=[validate_number, validate_year_period_min_length],
        )
    MONTH_PERIOD_CHOICES = [
        ('', ''),
        ('Jan', 'Январь'),
        ('Feb', 'Февраль'),
        ('Mar', 'Март'),
        ('Apr', 'Апрель'),
        ('May', 'Май'),
        ('Jun', 'Июнь'),
        ('Jul', 'Июль'),
        ('Aug', 'Август'),
        ('Sep', 'Сентябрь'),
        ('Oct', 'Октябрь'),
        ('Nov', 'Ноябрь'),
        ('Dec', 'Декабрь'),
        ]
    month_period = models.CharField(
        "Месяц",
        help_text="Выберите месяц, если начисления" 
        + " членских взносов расчитываются помесячно",
        max_length=3,
        blank=True,
        choices=MONTH_PERIOD_CHOICES,
        default='',
        )
    rate = models.DecimalField(
        "Размер взноса",
        help_text="Укажите размер членского взноса для выбранного" 
        + " периода в рублях за сотку (100 м.кв)",
        max_digits=7,
        decimal_places=2,
        )
    snt = models.ForeignKey(
        Snt,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="СНТ",
        help_text="Выберите СНТ для которого будет применен тариф",
        ) 

    class Meta:
        verbose_name = "Тариф (членский взнос)"
        verbose_name_plural = "Тарифы (членский взнос)"
        constraints = [
            models.UniqueConstraint(
                fields=['year_period', 'month_period'],
                name='%(app_label)s_%(class)s_year_month_period',
                )
            ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.year_period + " " + self.month_period

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass

class TPayment(models.Model):
    """Represents target payment with detailed information about target,
    amount, status and land plot."""
    payment_date = models.DateField(
        "Дата оплаты",
        help_text="Фактическая дата оплаты",
        blank=True,
        null=True,
        )
    target = models.CharField(
        "Цель",
        max_length=200,
        help_text="Укажите назначение целевого взноса",
        )
    amount = models.DecimalField(
        "Сумма",
        help_text="Сумма взноса к оплате",
        max_digits=7,
        decimal_places=2,
        )
    land_plot = models.ForeignKey(
        LandPlot,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Участок",
        help_text="Выберите участок",
        )
    STATUS_CHOICES = [
        ('n', 'Неоплачено'),
        ('p', 'Оплачено'),
        ('c', 'Оплата подтверждена'),
        ] 
    status = models.CharField(
        "Статус",
        max_length=1,
        choices=STATUS_CHOICES,
        default='n',
        help_text="Статус оплаты",
        ) 
 
    class Meta:
        verbose_name = "целевой взнос"
        verbose_name_plural = "целевые взносы"

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.target + " " + self.land_plot.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass


