from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q
from django.urls import reverse
from django.http import Http404

# Data validators
def validate_number(value):
    """Makes number validation (only numeric symbols)."""
    wrong_char_list = []
    for char in value:
        if ord(char) > 57 or ord(char) < 48:
            wrong_char_list.append(char)
    if wrong_char_list:
        wrong_string = ", ".join(wrong_char_list)
        raise ValidationError(
            _('Некорректный символ - (' + wrong_string + ')')
        )

def validate_phone(value):
    """Makes phone number validation."""
    wrong_char_list = []
    for char in value:
        if ord(char) > 57 or (ord(char) < 48 and ord(char) != 43):
            wrong_char_list.append(char)
    if wrong_char_list:
        wrong_string = ", ".join(wrong_char_list)
        raise ValidationError(
            _('Некорректный символ - (' + wrong_string + ')')
        )
    if value[0] != "+":
        raise ValidationError(
            _('Неверный формат номера - ' + value)
        )

def validate_20_length(value):
    """Makes 20 length number validation."""
    if len(value) < 20:
        raise ValidationError(
            _('Указанный номер меньше 20-и знаков')
        )

def validate_10_length(value):
    """Makes 10 length number validation."""
    if len(value) < 10:
        raise ValidationError(
            _('Указанный номер меньше 10-и знаков')
        )

def validate_9_length(value):
    """Makes 9 length numbers validation."""
    if len(value) < 9:
        raise ValidationError(
            _('Указанный номер меньше 9-и знаков')
        )

def validate_human_names(value):
    """Makes name validation (use only Russian letters)."""
    for char in value:
        if ord(char) < 1040 or ord(char) > 1103:
            raise ValidationError(
                _('Можно использовать только русские символы')
            )

def validate_accountant_user(value):
    """Makes User validation for Accountant model."""
    if Accountant.objects.filter(user__exact=value).exists():
        error_message = f"Бухгалтер с этим логином уже существует!"
        raise ValidationError(_(error_message))

def validate_owner_user(value):
    """Makes User validation for Owner model."""
    if Owner.objects.filter(user__exact=value).exists(): 
        error_message = f"Владелец с этим логином уже существует!"
        raise ValidationError(_(error_message))

def validate_chair_man_user(value):
    """Makes User validation for ChairMan model."""
    if ChairMan.objects.filter(user__exact=value).exists(): 
        error_message = f"Председатель с этим логином уже существует!"
        raise ValidationError(_(error_message))

def upload_directory(instance, filename):
    """Callable to create upload_to argument."""
    return 'docs/%Y/{0}/{1}'.format(instance.user.id, filename)

# Re-use helper functions
def chair_man_user_exists(user):
    """Checks that django.contrib.auth.models.User is not taken for
    ChairMan model's user field."""
    if user != None:
        if ChairMan.objects.filter(user__exact=user).exists():
            return True 

def accountant_user_exists(user):
    """Checks that django.contrib.auth.models.User is not taken for
    Accountant model's user field."""
    if user != None:
        if Accountant.objects.filter(user__exact=user).exists():
            return True 

def owner_user_exists(user):
    """Checks that django.contrib.auth.models.User is not taken for
    Owner model's user field."""
    if user != None:
        if Owner.objects.filter(user__exact=user).exists():
            return True 

#Create your models here.
class Snt(models.Model):
    """Model represents SNT with basic information such as
    SNT name, chairman, payment details, address."""
    name = models.CharField(
        "Название",
        max_length=200,
        help_text="Укажите только название без правовой организационной формы",
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
    address = models.CharField(
        "Адрес",
        max_length=200,
        help_text="Полный адрес садоводства включая область и р-он",
        )
    chair_man = models.OneToOneField(
        'ChairMan',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="председатель",
        help_text="председатель садоводства",
        )
    accountant = models.OneToOneField(
        'Accountant',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="бухгалтер",
        help_text="бухгалтер садоводства",
        )

    class Meta:
        verbose_name = "СНТ"
        verbose_name_plural = "СНТ"

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.name 
    
    def get_absolute_url(self): 
        """Returns url to access an instance of the model."""
        pass
        #return reverse('snt-detail', args=[str(self.id)])

    # Custom methods
    def clean_fields(self, exclude=None):
        """Custom method to check model form fields
        and restrict to have only one Snt in DB."""
        all_snt = Snt.objects.all()
        if len(all_snt) == 0:
            super().clean_fields(exclude=exclude)
        elif len(all_snt) == 1:
            if all_snt[0] == self:
                super().clean_fields(exclude=exclude)
            else:
                super().clean_fields(exclude=exclude)
                raise ValidationError({
                    'name': _(
                        'Разрешено создать только одно СНТ в базе данных'
                        ),
                    })


    def save(self, *args, **kwargs):
        """Before saving entry to db checks against 'only one entry allowed'."""
        all_snt = Snt.objects.all()
        if len(all_snt) == 0 or \
            (len(all_snt) == 1 and all_snt[0] == self):
            super().save(*args, **kwargs)
        else:
                raise Http404(
                     _("Разрешено создать только одно СНТ в базе данных")
                    )

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
        verbose_name="Владелец участка",
        help_text="Владелец участка",
        )   
   
    class Meta:
        verbose_name = "участок"
        verbose_name_plural = "участки"
        constraints = [
            models.UniqueConstraint(
                fields=['plot_number'],
                name='%(app_label)s_%(class)s_plot_number_unique_constraint',
                ),
            ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.plot_number

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        #return reverse('land-plot-detail', args=[str(self.id)])
        pass

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
    phone = models.CharField(
        "Номер телефона",
        max_length=12,
        help_text="Укажите номер в формате +7xxxxxxxxxx",
        unique=True,
        blank=True,
        null=True,
        validators=[validate_phone],
        )
    email = models.EmailField(
        "Почта",
        unique=True,
        blank=True,
        null=True,
        help_text="Адрес электронной почты",
        )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Логин",
        help_text="Аккаунт пользователя на сайте",
        validators=[validate_owner_user, validate_accountant_user],
        )
    join_date = models.DateField(
        "Дата вступления в должность",
        help_text="Укажите дату вступления в должность",
        )
    leave_date = models.DateField(
        "Дата ухода с должности",
        help_text="Укажите дату ухода с должности",
        blank=True,
        null=True,
        )
    class Meta:
        verbose_name = "председатель"
        verbose_name_plural = "председатели"
        constraints = [
            models.UniqueConstraint(
                fields=['join_date'],
                name='%(app_label)s_%(class)s_join_date_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['leave_date'],
                name='%(app_label)s_%(class)s_leave_date_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['email'],
                name='%(app_label)s_%(class)s_email_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['phone'],
                name='%(app_label)s_%(class)s_phone_unique_constraint',
                ),
      ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass
        #return reverse('chairman-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Custom save method to restrict to have only one chair man
        and prevent using same user for different models."""
        check_list = ChairMan.objects.filter(
            join_date__isnull=False,
            leave_date__isnull=True,
            ).all()
        if len(check_list) == 0 or \
            (len(check_list) == 1 and check_list[0] == self):
            if owner_user_exists(self.user):
                raise Http404(
                    _("Владелец с таким логином уже существует")
                    )
            elif accountant_user_exists(self.user):
                raise Http404(
                    _("Бухгалтер с таким логином уже существует")
                    )
            else:
                super().save(*args, **kwargs)
        else:
            raise Http404(
                _("Разрешено иметь только одного действующего бухгалтера")
                )

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
    phone = models.CharField(
        "Номер телефона",
        max_length=12,
        help_text="Укажите номер в формате +7xxxxxxxxxx",
        unique=True,
        blank=True,
        null=True,
        validators=[validate_phone],
        )

    email = models.EmailField(
        "Почта",
        unique=True,
        blank=True,
        null=True,
        help_text="Адрес электронной почты",
        )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Логин",
        help_text="Аккаунт пользователя на сайте",
        validators=[validate_accountant_user, validate_chair_man_user],
        )
    join_date = models.DateField(
        "Дата вступления в СНТ",
        help_text="Укажите дату вступления в члены СНТ",
        )
    leave_date = models.DateField(
        "Дата выхода из СНТ",
        help_text="Укажите дату выхода из членов СНТ",
        blank=True,
        null=True,
        )
   
    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "владельцы"
        constraints = [
           models.UniqueConstraint(
                fields=['email'],
                name='%(app_label)s_%(class)s_email_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['phone'],
                name='%(app_label)s_%(class)s_phone_unique_constraint',
                ),
           ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass
        #return reverse('owner-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Custom save method to restrict using same user for
        different models."""
        if chair_man_user_exists(self.user):
            raise Http404(
                _("Председатель с таким логином уже существует")
                )
        elif accountant_user_exists(self.user):
            raise Http404(
                _("Бухгалтер с таким логином уже существует")
                )
        else:
            super().save(*args, **kwargs)

class Accountant(models.Model):
    """Model representing snt accountant basic infromation
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
    phone = models.CharField(
        "Номер телефона",
        max_length=12,
        help_text="Укажите номер в формате +7xxxxxxxxxx",
        unique=True,
        blank=True,
        null=True,
        validators=[validate_phone],
        )

    email = models.EmailField(
        "Почта",
        unique=True,
        blank=True,
        null=True,
        help_text="Адрес электронной почты",
        )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Логин",
        help_text="Аккаунт пользователя на сайте",
        validators=[validate_owner_user, validate_chair_man_user]
        )
    join_date = models.DateField(
        "Дата вступления в должность",
        help_text="Укажите дату вступления в должность",
        )
    leave_date = models.DateField(
        "Дата ухода с должности",
        help_text="Укажите дату ухода с должности",
        blank=True,
        null=True,
        default=None,
        )
   
    class Meta:
        verbose_name = "бухгалтер"
        verbose_name_plural = "бухгалтеры"
        constraints = [
           models.UniqueConstraint(
                fields=['email'],
                name='%(app_label)s_%(class)s_email_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['phone'],
                name='%(app_label)s_%(class)s_phone_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['join_date'],
                name='%(app_label)s_%(class)s_join_date_unique_constraint',
                ),
            models.UniqueConstraint(
                fields=['leave_date'],
                name='%(app_label)s_%(class)s_leave_date_unique_constraint',
                ),
     ]

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass
        #return reverse('owner-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Custom save method to restrict to have only one accountant
        and prevent using same user for different models."""
        check_list = Accountant.objects.filter(
            join_date__isnull=False,
            leave_date__isnull=True,
            ).all()
        if len(check_list) == 0 or \
            (len(check_list) == 1 and check_list[0] == self):
            if owner_user_exists(self.user):
                raise Http404(
                    _("Владелец с таким логином уже существует")
                    )
            elif chair_man_user_exists(self.user):
                raise Http404(
                    _("Председатель с таким логином уже существует")
                    )
            else:
                super().save(*args, **kwargs)
        else:
            raise Http404(
                _("Разрешено иметь только одного действующего бухгалтера")
                )

class Docs(models.Model):
    """Represents different kinds of documents to be published on site."""
    upload_date = models.DateField(
        "Дата загрузки",
        auto_now_add=True,
        help_text="Дата загрузки документа",
        blank=True,
        )
    title = models.CharField(
        "Название документа",
        max_length=200,
        help_text="Укажите название документа",
        )
    
    docfile = models.ImageField(
        upload_to='documents/',
        verbose_name="Файл документа",
        help_text="Выберите файл для загрузки",
        )
    doc_user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        )
    STATUS_CHOICES = [
         ('published', 'Опубликовано'),
         ('unpublished', 'Неопубликовано'),
         ]
    status = models.CharField(
         "Статус",
         max_length=11,
         help_text="Выберите статус для публикации или снятия с публикации",
         choices=STATUS_CHOICES,
         default='unpublished',
         )

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.title

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        return reverse('docs-details', kwargs={"pk": str(self.id)})


class Info(models.Model):
    """Represents different kinds of information to be published on site."""
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        help_text="Дата и время публикации",
        blank=True,
        )
    title = models.CharField(
        "Заголовок",
        max_length=200,
        help_text="Заголовок объявления",
        )

    body = models.TextField(
        "Текст",
        help_text="Текст объявления",
        )
    author = models.ForeignKey(
        ChairMan, 
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Автор объявления (действующий председатель)",
        )
    STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('unpublished', 'Неопубликовано'),
        ]
    status = models.CharField(
        "Статус",
        max_length=11,
        help_text="Выберите статус для публикации или снятия с публикации",
        choices=STATUS_CHOICES,
        default='unpublished',
        )
    
    class Meta:
        verbose_name = "информация"
        verbose_name_plural = "информация"

    def __str__(self):
        """String to represent the Model(class) object."""
        return self.title

    def get_absolute_url(self):
        """Returns url to access an instance of the model."""
        pass
