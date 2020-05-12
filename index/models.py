from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q
from django.urls import reverse

# Data validators
def validate_number(value):
    """Makes number validation (use only numbers)."""
    wrong_char_list = []
    for char in value:
        if ord(char) > 57 or ord(char) < 48:
            wrong_char_list.append(char)
    if wrong_char_list:
        wrong_string = ", ".join(wrong_char_list)
        raise ValidationError(
            _('Некорректный символ - (' + wrong_string + ')')
        )

def validate_20_length(value):
    """Makes 20 length number validation."""
    if len(value) < 20:
        raise ValidationError(
            _('Неверный номер (меньше 20-и знаков)')
        )

def validate_10_length(value):
    """Makes 10 length number validation."""
    if len(value) < 10:
        raise ValidationError(
            _('Неверный номер (меньше 10-и знаков)')
        )

def validate_9_length(value):
    """Makes 9 length numbers validation."""
    if len(value) < 9:
        raise ValidationError(
            _('Неверный номер (меньше 9-и знаков)')
        )

def validate_human_names(value):
    """Makes name validation (use only Russian letters)."""
    for char in value:
        if ord(char) < 1040 or ord(char) > 1103:
            raise ValidationError(
                _('Можно использовать только русские символы')
            )

# Create your models here.
class Snt(models.Model):
    """Model representing a SNT with basic information such as
    SNT name, chairman, payment details, address."""
    name = models.CharField(
        "Название СНТ",
        max_length=200,
        help_text="Полное название СНТ",
    )
    personal_acc = models.CharField(
        "Номер расчетного счета",
        max_length=20,
        help_text="Номер расчетного счета (20-и значное число)",
        validators=[validate_number, validate_20_length],
    )
    bank_name = models.CharField(
        "Наименование банка получателя",
        max_length=45,
        help_text="Наименование банка получателя",
    )
    bic = models.CharField(
        "БИК",
        max_length=9,
        help_text="БИК (9-и значное число)",
        validators=[validate_number, validate_9_length],
    )
    corresp_acc = models.CharField(
        "Номер кор./счета",
        max_length=20,
        help_text="Номер кор./счета (20-и значное число)",
        validators=[validate_number, validate_20_length],
    )
    inn = models.CharField(
        "ИНН",
        max_length=10,
        help_text="ИНН (10-и значное число)",
        validators=[validate_number, validate_10_length],
    )
    kpp = models.CharField(
        "КПП",
        max_length=9,
        help_text="КПП (9-и значное число)",
        validators=[validate_number, validate_9_length],
    )
    chair_man = models.OneToOneField(
        'ChairMan',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='председатель',
        help_text="Председатель садоводства",
    )

    class Meta:
        verbose_name = "СНТ"
        verbose_name_plural = "СНТ"

    def __str__(self):
        """String for representing the Model object."""
        return self.name 
    
    def get_absolute_url(self): 
        """Returns the url to access a detail record for this snt.""" 
        return reverse('snt-detail', args=[str(self.id)])

class LandPlot(models.Model):
    """Model representing a land plot with basic information
    such as plot number (unique), area, owners (many-to-many), 
    snt (fk), electrical counter (one-to-one), user."""
    plot_number = models.CharField(
        "Номер участка",
        max_length=10,
        help_text="Номер участка",
        unique=True,
        )
    plot_area = models.PositiveIntegerField(
        "Размер участка",
        help_text="Единица измерения кв.м",
        )
    snt = models.ForeignKey(
       Snt,
       on_delete=models.SET_NULL,
       null=True,
       verbose_name="СНТ",
       help_text="Расположен в СНТ",
       ) 
    owner = models.ForeignKey(
        'Owner',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="владелец участка",
        help_text="Владелец участка",
        )   
    electrical_counter = models.OneToOneField(
        'ElectricalCounter',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Счетчик',
        help_text="Данные прибора учета электроэнергии",
        )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Логин",
        help_text="Аккаунт пользователя на сайте",
        )
    
    class Meta:
        verbose_name = "участок"
        verbose_name_plural = "участки"

    def __str__(self):
        """String for representing the Model object."""
        return self.plot_number

    def get_absolute_url(self):
        """Returns the url to access a detail record for land plot."""
        return reverse('land-plot-detail', args=[str(self.id)])

class ChairMan(models.Model):
    """Model representing a chairman of snt with basic information
    such as first name, last name, status (current or former)
    hire date, retire date, snt (one-to-one)."""
    first_name = models.CharField(
        "Имя",
        max_length=50,
        help_text="Введите имя",
        validators = [validate_human_names],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=50,
        help_text="Введите отчество",
        validators = [validate_human_names],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
        help_text="Введите фамилию",
        validators = [validate_human_names],
    )

    class Meta:
        verbose_name = "председатель"
        verbose_name_plural = "председатели"

    def __str__(self):
        """String for representing the Model object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('chairman-detail', args=[str(self.id)])

class Owner(models.Model):
    """Model representing an owner of land plot with basic infromation
    such as first name, last name, status (current or former), 
    land plot (many-to-many), start owner date, end owner date."""
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
        help_text="Введите фамилию",
        validators = [validate_human_names],
    )
    first_name = models.CharField(
        "Имя",
        max_length=50,
        help_text="Введите имя",
        validators = [validate_human_names],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=50,
        help_text="Введите отчество",
        validators = [validate_human_names],
    )
    OWNER_STATUS = [
        ('c', 'Настоящий'),
        ('p', 'Прежний'),
    ]
    status = models.CharField(
        "Статус владельца",
        max_length=1,
        choices=OWNER_STATUS,
        default='c',
        help_text="Статус владельца",
    )
    start_owner_date = models.DateField(
        verbose_name="дата начала владения",
    )
    end_owner_date = models.DateField(
        verbose_name="дата окончания владения",
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "владельцы"

    def __str__(self):
        """String for representing the Model object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('owner-detail', args=[str(self.id)])
