from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from index.models import LandPlot, Snt
from membership.validators import *
from decimal import *

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
        #blank=True,
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
        ('not_paid', 'Неоплачено'),
        ('paid', 'Оплачено'),
        ('payment_confirmed', 'Оплата подтверждена'),
        ] 
    status = models.CharField(
        "Статус",
        max_length=17,
        choices=STATUS_CHOICES,
        default='not_paid',
        help_text="Статус оплаты",
    ) 
    class Meta:
        verbose_name = "членский взнос"
        verbose_name_plural = "членские взносы"
        constraints = [
            models.UniqueConstraint(
                fields=['year_period', 'month_period', 'land_plot'],
                name='%(app_label)s_%(class)s_year_month_period_land_plot'
                    + '_unique_constraint',
                )
            ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.year_period + " " + self.land_plot.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass


     # Custom methods
    def calculate(self):
        """Calculates e_payment."""
        rate = MRate.objects.filter(
            year_period__exact=self.year_period,
            month_period__exact=self.month_period,
            ).get()
        self.plot_area = self.land_plot.plot_area
        self.rate = rate.rate
        self.amount = Decimal(self.plot_area / 100) * self.rate

    def save(self, *args, **kwargs):
        """Custom save method."""
        if self.status == 'not_paid':
            self.calculate()
        super().save(*args, **kwargs)
    
    def create_qr_text(self):
        """Create qr_text to generate payment QR code."""
        # Prepare purpose text
        if self.s_new != None:
            purpose = f"Членские взносы за э/энергию, однотарифный"
            purpose += f"/{self.s_new}-{self.s_prev}/{self.s_cons}, "
            purpose += f"{self.s_cons}x{self.s_amount/self.s_cons}/"
            purpose += f"{self.s_amount}. Итого/{self.sum_total}."
        elif self.t1_new != None and self.t2_new != None:
            purpose = f"Членские взносы за э/энергию, "
            purpose += f"T1/{self.t1_new}-{self.t1_prev}/{self.t1_cons}, " 
            purpose += f"T2/{self.t2_new}-{self.t2_prev}/{self.t2_cons}, " 
            purpose += f"T1/{self.t1_cons}x{self.t1_amount/self.t1_cons}/"
            purpose += f"{self.t1_amount}, " 
            purpose += f"T2/{self.t2_cons}x{self.t2_amount/self.t2_cons}/"
            purpose += f"{self.t2_amount}. Итого/{self.sum_total}." 
        # Prepare payer address text
        payer_address = f"участок №{self.land_plot.plot_number}, "
        payer_address += f"СНТ \"{self.land_plot.snt.name}\""   
        # Prepare qr text
        qr_text = f"ST00012|"
        qr_text += f"Name=Садоводческое некоммерческое товарищество "
        qr_text += f"\"{self.land_plot.snt.name}\"|"
        qr_text += f"PersonalAcc={self.land_plot.snt.personal_acc}|"
        qr_text += f"BankName={self.land_plot.snt.bank_name}|"
        qr_text += f"BIC={self.land_plot.snt.bic}|"
        qr_text += f"CorrespAcc={self.land_plot.snt.corresp_acc}|"
        qr_text += f"INN={self.land_plot.snt.inn}|"
        qr_text += f"LastName={self.land_plot.owner.last_name}|"
        qr_text += f"FirstName={self.land_plot.owner.first_name}|"
        qr_text += f"MiddleName={self.land_plot.owner.middle_name}|"
        qr_text += f"Purpose={purpose}|"
        qr_text += f"PayerAddress={payer_address}|"
        qr_text += f"Sum={int(self.sum_total * 100)}"
        return qr_text
    
    def paid(self):
        """Set EPayment status to 'paid'."""
        if self.status == 'not_paid':
            self.status = 'paid'
            self.payment_date = datetime.date.today()
            self.save()
    
    def payment_confirmed(self):
        """Set EPayment status to 'payment_confirmed'."""
        if self.status == 'paid':
            self.status = 'payment_confirmed'
            self.save()

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
        #blank=True,
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
                name='%(app_label)s_%(class)s_year_month_period_constraint',
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
        ('not_paid', 'Неоплачено'),
        ('paid', 'Оплачено'),
        ('payment_confirmed', 'Оплата подтверждена'),
        ] 
    status = models.CharField(
        "Статус",
        max_length=17,
        choices=STATUS_CHOICES,
        default='not_paid',
        help_text="Статус оплаты",
        ) 
 
    class Meta:
        verbose_name = "целевой взнос"
        verbose_name_plural = "целевые взносы"
        constraints = [
            models.UniqueConstraint(
                fields=['target', 'land_plot'],
                name='%(app_label)s_%(class)s_target_land_plot_unique_constraint',
                )
            ] 

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.target + " " + self.land_plot.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass


