﻿from django.db import models
from django.db.models import Q
from index.models import Snt, LandPlot
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

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
        "Один тариф",
        help_text="Показания э/счетчика (один тариф) на момент"
        + " установки/приемки к учету в веб приложении",
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

    # Model custom methods
    def is_single(self):
        """Checks if model type is "single"."""
        if self.model_type == "single":
            return True
        else:
            return False

    def is_double(self):
        """Checks if model type is "single"."""
        if self.model_type == "double":
            return True
        else:
            return False

    def single_type_fields_ok(self):
        """Validates data in s, t1 and t2 fields for single type model."""
        error = ""
        if self.s == None:
            error = "Необходимо указать показания э/счетчика (один тариф)"\
                + " на момент установки/приемки к учету в веб приложении"
        if len(error) > 0:
            raise ValidationError(_(error))
        else:
            return True

    def double_type_fields_ok(self):
        """Validates data in s, t1 and t2 fields for double type model."""
        error = "" 
        if self.t1 == None:
            error += "Необходимо указать показания э/счетчика тариф Т1 (день)"\
                + " на момент установки/приемки к учету в веб приложении"
        if self.t2 == None:
            error += "Необходимо указать показания э/счетчика тариф Т2 (ночь)"\
                + " на момент установки/приемки к учету в веб приложении"
        if len(error) > 0:
            raise ValidationError(_(error))
        else:
            return True

    def save(self, *args, **kwargs):
        """Custom save method to prevent error in s, t1, t2, model_type fields."""
        if self.is_single():
            if self.single_type_fields_ok() == True:
                self.t1 == None
                self.t2 == None
                super().save(*args, **kwargs)
        if self.is_double():
            if self.double_type_fields_ok() == True:
                self.s = None
                super().save(*args, **kwargs)

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
    land_plot = models.ForeignKey(
        LandPlot,
        verbose_name="Участок",
        help_text="Выберите участок",
        on_delete=models.SET_NULL,
        null=True,
        )
    e_counter = models.ForeignKey(
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
                    + '_unique_constraint'
                )
            ]

    def __str__(self):
         """String to represent the Model(class) object."""
         return str(self.rec_date) + " уч-" + self.land_plot.plot_number

    def get_absolute_url(self):
         """Returns url to access an instance of the model."""
         pass

    # Model custom methods
    # Custom save() method and help methods for data evaluation
    def save(self, *args, **kwargs):
        """Custom save method checks fields data before saving."""
        model_type = ""
        if self.e_counter.model_type == "single":
            if self.e_counter_single_type_fields_ok() == True:
                model_type = "single"
                self.t1 = None
                self.t2 = None
                if self.check_vs_latest_record(self.get_latest_record(), model_type):
                    super().save(*args, **kwargs)
        elif self.e_counter.model_type == "double":
            if self.e_counter_double_type_fields_ok() == True:
                model_type = "double"
                self.s = None
                if self.check_vs_latest_record(self.get_latest_record(), model_type):
                    super().save(*args, **kwargs)
    
    def records_exist(self):
        """Checks if any records already exist in database for
        LandPlot and ECounter."""
        query_set = ECounterRecord.objects.filter(
            land_plot__exact=self.land_plot,
            e_counter__exact=self.e_counter,
            ).all()
        if len(query_set) > 0:
            return True
        else:
            return False

    def e_counter_single_type_fields_ok(self):
        """Validates data in s, t1 and t2 fields to conform with
        field object property e_counter.model_type="single"."""
        error = ""
        if self.s == None:
            error = "Необходимо указать показания э/счетчика (один тариф)"
        if len(error) > 0:
            raise ValidationError(_(error))
        else:
            return True

    def e_counter_double_type_fields_ok(self):
        """Validates data in s, t1 and t2 fields to conform with
        field object property e_counter.model_type="double"."""
        error = "" 
        if self.t1 == None:
            error += "Необходимо указать показания э/счетчика тариф Т1 (день)"
        if self.t2 == None:
            error += "Необходимо указать показания э/счетчика тариф Т2 (ночь)"
        if len(error) > 0:
            raise ValidationError(_(error))
        else:
            return True

    def get_latest_record(self):
        """Returns latest electrical counter record from database
        filtered by latest date, land plot and electrical counter."""
        if self.records_exist():
            latest_record = ECounterRecord.objects.filter(
                land_plot__exact=self.land_plot,
                e_counter__exact=self.e_counter,
                ).latest('rec_date')
            return latest_record
    
    def single_error_message(self, new_s, old_s):
        """Create error message for different model types wrong data."""
        message = f"Новое показание {new_s} должно быть больше предыдущего {old_s}"
        return message
     
    def double_error_message(self, new_t1, old_t1, new_t2, old_t2):
        """Create error message for different model types wrong data."""
        message = f"Новые показания должны быть больше старых. "
        message += f"День: {new_t1} > {old_t1}. Ночь: {new_t2} > {old_t2}."
        return message

    def check_vs_latest_record(self, latest_record, model_type):
        """Checks that new record fields data bigger than latest record."""
        # If now records exist in db, checks new record vs e_counter
        if latest_record == None:
            if model_type == "single":
                if self.s > self.e_counter.s:
                    return True
                else:
                    error = self.single_error_message(self.s, self.e_counter.s)
                    raise ValidationError(_(error))
            elif model_type == "double":
                if self.t1 > self.e_counter.t1 and self.t2 > self.e_counter.t2:
                    return True
                else:
                    error = self.double_error_message(
                        self.t1, self.e_counter.t1,
                        self.t2, self.e_counter.t2
                        )
                    raise ValidationError(_(error))
        # If records exist in db
        elif model_type == "single":
            if self.s > latest_record.s:
                return True
            else:
                error = self.single_error_message(self.s, latest_record.s)
                raise ValidationError(_(error))
        elif model_type == "double":
            if self.t1 > latest_record.t1 and self.t2 > latest_record.t2:
                return True
            else:
                error = self.double_error_message(
                        self.t1, latest_record.t1,
                        self.t2, latest_record.t2
                        )
                raise ValidationError(_(error))
    
    # create_e_payment() method
    def no_e_payment(self):
        """Checks that e_counter_record has no e_payment record."""
        if EPayment.objects.filter(
            e_counter_record__exact=self,
            ).exists():
            return False
        else:
            return True

    def e_payments_exist(self):
        """Check if any e_payment exist in db for self.land_plot and
        self.e_counter."""
        if EPayment.objects.filter(
            land_plot__exact=self.land_plot,
            e_counter_record__e_counter__exact=self.e_counter,
            ).exists():
            return True
        else:
            return False

    def no_unpaid_and_paid_payments(self):
        """Checks that there is no e_payment records in db
        for self.land_plot and self.e_counter with 'unpaid' and
        'paid' status."""
        if EPayment.objects.filter(
            Q(status='not_paid') | Q(status='paid'),
            land_plot__exact=self.land_plot,
            e_counter_record__e_counter__exact=self.e_counter,
            ).exists():
            return False
        else:
            return True

    def last_payment_confirmed_e_counter_record(self):
        """Returns last e_counter_record where e_payment exists and
        e_payment status is payment_confirmed."""
        last_e_payment = EPayment.objects.filter(
            land_plot__exact=self.land_plot,
            e_counter_record__e_counter__exact=self.e_counter,
            status="payment_confirmed",
            ).latest('payment_date')
        return last_e_payment.e_counter_record


    def create_e_payment(self):
        """Creates EPayment record in db."""
        if self.no_e_payment():
            if self.e_payments_exist():
                if self.no_unpaid_and_paid_payments():
                    last_rec = self.last_payment_confirmed_e_counter_record()
                    EPayment.objects.create(
                        s_new=self.s,
                        t1_new=self.t1,
                        t2_new=self.t2,
                        s_prev=last_rec.s,
                        t1_prev=last_rec.t1,
                        t2_prev=last_rec.t2,
                        land_plot=self.land_plot,
                        e_counter_record=self,
                        )
                    ECounterRecord.objects.filter(
                        land_plot__exact=self.land_plot,
                        e_counter__exact=self.e_counter,
                        rec_date__lt=self.rec_date,
                        rec_date__gt=last_rec.rec_date,
                        ).delete()
                else:
                    raise ValidationError(_("not all payment confirmed"))
            else:
                EPayment.objects.create(
                    s_new=self.s,
                    t1_new=self.t1,
                    t2_new=self.t2,
                    s_prev=self.e_counter.s,
                    t1_prev=self.e_counter.t1,
                    t2_prev=self.e_counter.t2,
                    land_plot=self.land_plot,
                    e_counter_record=self,
                    )
        else:
            raise ValidationError(_("e_payment_already_exist"))
 
    
class ERate(models.Model):
    """Represents electricity rate in rub per 1kwh to make
    payment calculation for consumed electricity."""
    date = models.DateField(
        "Дата",
        help_text="Текущая дата будет использована автоматически"
        + " для нового тарифа за электроэнергию",
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
         constraints = [
            models.UniqueConstraint(
                fields=['date'],
                name='%(app_label)s_%(class)s_date_unique_constraint'
                ),
            models.CheckConstraint(
                check=models.Q(date__gte=datetime.date.today()),
                name='%(app_label)s_%(class)s_date_greater_or_equal_today'
                    + '_constraint'
                )
            ]

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
    land_plot = models.ForeignKey(
        LandPlot,
        verbose_name="Участок",
        help_text="Выберите участок",
        on_delete=models.SET_NULL,
        null=True,
        )
    e_counter_record = models.OneToOneField(
        ECounterRecord,
        verbose_name="Запись показаний э/счетчика",
        help_text="Выберите запись показаний э/счетчика",
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
    
    # Custom methods
    def calculate(self):
        """Calculates e_payment."""
        rate = ERate.objects.latest('date')
        if self.s_new != None and self.s_prev != None:
            self.s_cons = self.s_new - self.s_prev
            self.s_amount = self.s_cons * rate.s
            self.sum_total = self.s_amount
        elif self.t1_new != None and self.t1_prev != None\
            and self.t2_new != None and self.t2_prev != None:
            self.t1_cons = self.t1_new - self.t1_prev
            self.t2_cons = self.t2_new - self.t2_prev
            self.t1_amount = self.t1_cons * rate.t1
            self.t2_amount = self.t2_cons * rate.t2
            self.sum_total = self.t1_amount + self.t2_amount
        else:
            self.s_cons = None
            self.t1_cons = None
            self.t2_cons = None
            self.s_amount = None
            self.t1_amount = None
            self.t2_amount = None
            self.sum_total = 0

    def save(self, *args, **kwargs):
        """Custom save method."""
        if self.status != 'payment_confirmed' or self.status != 'paid':
            self.calculate()
        super().save(*args, **kwargs)
    
    def create_qr_text(self):
    """Function to prepare qr code and return result to view
    for rendering web page (context{}, correct(bolean))."""
    qr_text = "ST00012|Name=Садоводческое некоммерческое товаричество \"{}\"|\
        PersonalAcc={}|BankName={}|BIC={}|CorrespAcc={}|INN={}|LastName={}|\
        FirstName={}|MiddleName={}|Purpose={}|PayerAddress={}|Sum={}"
    snt_name = el_payment_obj.land_plot.snt
    name = el_payment_obj.land_plot.snt
    p_acc = el_payment_obj.land_plot.snt.personal_acc
    b_name = el_payment_obj.land_plot.snt.bank_name
    bic = el_payment_obj.land_plot.snt.bic
    cor_acc = el_payment_obj.land_plot.snt.corresp_acc
    inn = el_payment_obj.land_plot.snt.inn
    last_name = el_payment_obj.land_plot.owner.last_name
    first_name = el_payment_obj.land_plot.owner.first_name
    middle_name = el_payment_obj.land_plot.owner.middle_name
    e_counter_type = el_payment_obj.land_plot.electrical_counter.model_type
    purpose = get_payment_purpose(el_payment_obj)
    payer_address = "участок №{}, СНТ {}".format(plot_num, name)   
    sum_tot = el_payment_obj.sum_tot * 100
    qr_text = qr_text.format(
        name, p_acc, b_name, bic, cor_acc,inn, last_name, first_name,
        middle_name, purpose, payer_address, sum_tot,
        )
    context = {
        'snt_name': snt_name,
        'el_payment_obj': el_payment_obj,
        'qr_text': qr_text,
        'payer_address': payer_address,
        'purpose': purpose,
        'last_name': last_name,
        'first_name': first_name,
        'middle_name': middle_name,
        }
    return qr_text
    

