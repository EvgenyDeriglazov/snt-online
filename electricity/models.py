from django.db import models
from index.models import Snt, LandPlot

# Create your models here.
class ECounter(models.Model):
    """Draft model for electrical counter."""
    reg_date = models.DateField(
        "Дата регистрации",
        help_text="Укажите дату установки нового э/счетчика"
        + " или приемки к учету в веб приложении уже имеющегося",
        )
    model_name = models.CharField(
        "Название модели",
        max_length=100,
        help_text="Укажите название модели э/счетчика"
        )
    sn = models.CharField(
        "Серийный номер",
        max_length=50,
        help_text="Укажите серийный номер э/счетчика",
        )
    MODEL_TYPE_CHOICES = [
        ('single', 'Однотарифный'),
        ('double', 'Двухтарифный'),
        ]
    model_type = models.CharField(
        "Тип",
        max_length=6,
        help_text="Выберите тип э/счетчика",
        choices=MODEL_TYPE_CHOICES,
        )
    s = models.PositiveIntegerField(
        "Однотарифный",
        help_text="Показания э/счетчика на момент установки"
        + "/приемки к учету в веб приложении",
        blank=True,
        null=True,
        )
    t1 = models.PositiveIntegerField(
        "День",
        help_text="Показания э/счетчика тариф Т1 (день)"
        + " на момент установки/приемки к учету в веб приложении",
        blank=True,
        null=True,
        )
    t2 = models.PositiveIntegerField(
        "Ночь",
        help_text="Показания э/счетчика тариф Т2 (ночь)"
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
         verbose_name = "счетчик э/энергии"
         verbose_name_plural = "счетчики э/энергии"
         constraints = [
            models.UniqueConstraint(
                fields=['model_name', 'sn'],
                name='%(app_label)s_%(class)s_model_name_sn_unique_constraint',
                )
            ]

    def __str__(self):
         """String to represent the Model(class) object."""
         return self.model_name

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

class ECounterRecord(models.Model):
    """Represents electrical counter readings records in kwh
    to control electrical consumption and calculate payment."""
    rec_date = models.DateField(
        "Дата показаний",
        help_text="Текущая дата будет использована автоматически"
        + " для сохранения показаний",
        auto_now_add=True,
        )
    s = models.PositiveIntegerField(
        "Однотарифный",
        help_text="Внесите показания э/счетчика (однотарифный)",
        blank=True,
        null=True,
        )
    t1 = models.PositiveIntegerField(
        "День",
        help_text="Внесите показания э/счетчика тариф Т1 (день)",
        blank=True,
        null=True,
        )
    t2 = models.PositiveIntegerField(
        "Ночь",
        help_text="Внесите показания э/счетчика тариф Т2 (ночь)",
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
    e_counter = models.OneToOneField(
        ECounter,
        verbose_name="Счетчик",
        help_text="Выберите счетчик",
        on_delete=models.SET_NULL,
        null=True,
        )

    class Meta:
         verbose_name = "показания э/счетчика"
         verbose_name_plural = "показания э/счетчиков"
         constraints = [
            models.UniqueConstraint(
                fields=['rec_date', 'land_plot', 'e_counter'],
                name='%(app_label)s_%(class)s_rec_date_land_plot_e_counter'
                    + '_unique_constraint',
                )
            ]

    def __str__(self):
         """String to represent the Model(class) object."""
         return str(self.rec_date) + " уч-" + self.land_plot.plot_number

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

class ERate(models.Model):
    """Represents electricity rate in rub per 1kwh to make
    payment calculation for consumed electricity."""
    date = models.DateField(
        "Дата",
        help_text="Текущая дата будет использована автоматически"
        + " для нового тарифа за электроэнергию",
        auto_now_add=True,
        )
    s = models.DecimalField(
        "Однотарифный",
        help_text="Рублей за один кВт/ч для однотарифного э/счетчика",
        max_digits=7,
        decimal_places=2,
        )
    t1 = models.DecimalField(
        "День",
        help_text="Рублей за один кВт/ч для тарифа Т1 (день)",
        max_digits=7,
        decimal_places=2,
        )
    t2 = models.DecimalField(
        "Ночь",
        help_text="Рублей за один кВт/ч для тарифа Т2 (ночь)",
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
         verbose_name = "тариф за э/энергию"
         verbose_name_plural = "тарифы за э/энергию"

    def __str__(self):
         """String to represent the Model(class) object."""
         return str(self.date)

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

class EPayment(models.Model):
    """Represents electricity payment records with all details
    for specific land plot. Can be used to generate paper 
    receipt or QR code."""
    payment_date = models.DateField(
        "Дата оплаты",
        help_text="Фактическая дата оплаты",
        blank=True,
        null=True,
        )
    s_new = models.PositiveIntegerField(
        "Текущее показание (однотарифный)",
        help_text="Текущее показание э/счетчика (однотарифный) кВт/ч",
        blank=True,
        null=True,
        )
    t1_new = models.PositiveIntegerField(
        "Текущее показание (день)",
        help_text="Текущее показание э/счетчика тариф Т1 (день) кВт/ч",
        blank=True,
        null=True,
        )
    t2_new = models.PositiveIntegerField(
        "Текущее показание (ночь)",
        help_text="Текущее показание э/счетчика тариф Т2 (ночь) кВт/ч",
        blank=True,
        null=True,
        )
    s_prev = models.PositiveIntegerField(
        "Предыдущее показание (однотарифный)",
        help_text="Предыдущее показание э/счетчика (однотарифный) кВт/ч",
        blank=True,
        null=True,
        )
    t1_prev = models.PositiveIntegerField(
        "Предыдущее показание (день)",
        help_text="Предыдущее показание э/счетчика тариф Т1 (день) кВт/ч",
        blank=True,
        null=True,
        )
    t2_prev = models.PositiveIntegerField(
        "Предыдущее показание (ночь)",
        help_text="Предыдущее показание э/счетчика тариф Т2 (ночь) кВт/ч",
        blank=True,
        null=True,
        )
    s_cons = models.PositiveIntegerField(
        "Расход (однотарифный)",
        help_text="Расход кВт/ч (однотарифный)",
        blank=True,
        null=True,
        )
    t1_cons = models.PositiveIntegerField(
        "Расход (день)",
        help_text="Расход кВт/ч тариф Т1 (день)",
        blank=True,
        null=True,
        )
    t2_cons = models.PositiveIntegerField(
        "Расход (ночь)",
        help_text="Расход кВт/ч тариф Т2 (ночь)",
        blank=True,
        null=True,
        )
    s_amount = models.DecimalField(
        "Сумма (однотарифный)",
        help_text="Сумма (однотарифный)",
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        )
    t1_amount = models.DecimalField(
        "Сумма (день)",
        help_text="Сумма тариф Т1 (день)",
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        )
    t2_amount = models.DecimalField(
        "Сумма (ночь)",
        help_text="Сумма тариф Т2 (ночь)",
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        )
    sum_total = models.DecimalField(
        "Итого",
        help_text="Итого",
        max_digits=8,
        decimal_places=2,
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
    land_plot = models.OneToOneField(
        LandPlot,
        verbose_name="Участок",
        help_text="Выберите участок",
        on_delete=models.SET_NULL,
        null=True,
        )
    class Meta:
         verbose_name = "взнос за э/энергию"
         verbose_name_plural = "взонсы за э/энергию"

    def __str__(self):
         """String to represent the Model(class) object."""
         return str(self.payment_date) + "-" + self.land_plot.plot_number

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

