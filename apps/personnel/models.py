from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.iranian_cities.fields import OstanField, ShahrestanField
from helpers.models import BaseModel

User = get_user_model()


class Profile(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    class DemandStatus(models.TextChoices):
        ACCEPTED = 'A', _('Accepted')
        REJECTED = 'R', _('Rejected')
        DRAFT = 'D', _('Draft')

    class MilitaryServiceStatus(models.TextChoices):  # وضعیت نظام وظیفه
        END_MILITARY = 'D', _('End Duty')  # پایان خدمت
        PERMANENT = 'P', _('Permanent')  # معافیت دائم
        SOLDIER = 'S', _('Soldier')  # سرباز
        EDUCATION_EXEMPTION = 'E', _('Education Exemption')  # معافیت تحصیلی
        MEDICAL_EXEMPTION = 'M', _('Medical Exemption')  # معافیت پزشکی
        SPONSORSHIP_EXEMPTION = 'N', _('Sponsorship Exemption')  # معافیت کفالت

    class MartialStatus(models.TextChoices):  # وضعیت تاهل
        EMPTY_CHOICE = ('', _('-------'))
        MARRIED = 'M', _('Married')
        SINGLE = 'S', _('Single')

    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name=_('Gender'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles', verbose_name=_('user'))
    father_name = models.CharField(max_length=250, verbose_name=_('Father Name'))
    birth_certificate_id = models.CharField(max_length=50, verbose_name=_('Birth Certificate id'))  # شماره شناسنامه
    birthdate = models.DateField(verbose_name=_('Birthdate'))
    birthdate_province = OstanField(related_name='birthdate_province')
    birthdate_city = ShahrestanField(related_name='birthdate_cities')
    issue_place = ShahrestanField(related_name='issue_places')
    first_page_certificate_image = models.ImageField(
        upload_to='personnel/profile/first_certificate_image', verbose_name='first page certificate image'
    )
    second_page_certificate_image = models.ImageField(
        upload_to='personnel/profile/second_certificate_image', verbose_name='second page certificate image'
    )
    third_page_certificate_image = models.ImageField(
        upload_to='personnel/profile/third_certificate_image', verbose_name='third page certificate image'
    )
    forth_page_certificate_image = models.ImageField(
        upload_to='personnel/profile/forth_certificate_image', verbose_name='forth page certificate image'
    )
    fifth_page_certificate_image = models.ImageField(
        upload_to='personnel/profile/fifth_certificate_image', verbose_name='fifth page certificate image'
    )
    front_identify_card_image = models.ImageField(
        upload_to='personnel/profile/front_identify_card_image', verbose_name=_('front identify card image')
    )  # عکس جلو کارت ملی
    back_identify_card_image = models.ImageField(
        upload_to='personnel/profile/back_identify_card_image', verbose_name=_('back identify card image')
    )  # عکس پشت کارت ملی
    military_service_status = models.CharField(
        max_length=1, null=False, choices=MilitaryServiceStatus.choices, verbose_name=_('Military Services Status')
    )
    military_service_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/military_service_image',
        verbose_name='military service image',
    )
    martial_status = models.CharField(
        max_length=1,
        choices=MartialStatus.choices,
        default=MartialStatus.EMPTY_CHOICE,
        verbose_name=_('Martial Status'),
    )
    province = OstanField(related_name='provinces', verbose_name='province')
    city = ShahrestanField(related_name='cities', verbose_name='city')
    address = models.TextField(verbose_name=_('Address'))
    postal_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^[0-9]{10}$', message=_('invalid postal code'))],
        verbose_name=_('Postal Code'),
    )
    telephone = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^0[0-9]{2,}[0-9]{7,}$', message=_('invalid telephone'))],
        verbose_name=_('Telephone'),
    )
    emergency_telephone = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^0[0-9]{2,}[0-9]{7,}$', message=_('invalid emergency telephone'))],
        verbose_name=_('Emergency Telephone'),
    )
    demand_status = models.CharField(
        max_length=1, choices=DemandStatus.choices, default=DemandStatus.DRAFT, verbose_name=_('Demand Status')
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Education(BaseModel):
    class Level(models.TextChoices):  # میزان تحصیلات
        EMPTY_CHOICE = ('', _('-------'))
        ILLITERATE = 'I', _('Illiterate')  # بی سواد
        SECONDARY_EDUCATION = 'S', _('Secondary Education')  # سیکل
        DIPLOMA = 'O', _('Diploma')  # دیپلم
        ASSOCIATE = 'A', _('Associate')  # فوق دیپلم
        BACHELOR = 'B', _('Bachelor')  # لیسانس
        MASTER = (
            'M',
            _('Master'),  # فوق لیسانس
        )
        DOCTORATE = 'D', _('Doctorate')  # دکترا
        POST_DOCTORAL = 'P', _('Post Doctoral')  # فوق دکترا

    class StudyField(models.TextChoices):
        EMPTY_CHOICE = ('', _('-------'))
        ACCOUNTANCY = 'AC', _('Accountancy')
        CIVIL_ENGINEERING = 'CI', _('Civil Engineering')
        COMPUTER_ENGINEERING = 'CO', _('COMPUTER Technology')
        ELECTRONICS = 'EL', _('Electronics')
        INDUSTRIAL_ENGINEERING = 'IN', _('Industrial Engineering')
        MECHANIC_ENGINEERING = 'ME', _('Mechanic Engineering')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations', verbose_name=_('user'))
    level = models.CharField(max_length=1, choices=Level.choices, default=Level.EMPTY_CHOICE, verbose_name=_('Level'))
    field = models.CharField(
        max_length=2, choices=StudyField.choices, default=Level.EMPTY_CHOICE, verbose_name=_('Field')
    )
    graduation_date = models.CharField(max_length=4, verbose_name=_('Graduation Date'))
    graduation_image = models.ImageField(
        upload_to='personnel/profile/graduation_image', verbose_name='Graduation Image'
    )

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')


class Bank(BaseModel):
    class Name(models.TextChoices):
        EMPTY_CHOICE = ('', _('-------'))
        ANSAR = '0', _('Ansar Bank')
        DEY = '1', _('Dey Bank')
        EGHTESAD_NOVIN = '2', _('Eghtesad Novin Bank')
        GARDESHGARI = '3', _('Gardeshgari Bank')
        GHAVAMIN = '4', _('Ghavamin Bank')
        HEKMAT_IRANIAN = '5', _('Hekmat Iranian Bank')
        IRAN_ZAMIN = '6', _('Iran Zamin Bank')
        KARAFARIN = '7', _('Karafarin Bank')
        KHAVARMIANEH = '8', _('Khavarmianeh Bank')
        KESHAVARZI = '9', _('Keshavarzi Bank')
        MASKAN = '10', _('Maskan Bank')
        MEHR_IRAN_GHARZOLHASANEH = '11', _('Mehr Iran Gharzolhasaneh Bank')
        MELLI = '12', _('Melli Bank')
        MELLAT = '13', _('Mellat Bank')
        PARSIAN = '14', _('Parsian Bank')
        PASARGAD = '15', _('Pasargad Bank')
        POST = '16', _('Post Bank')
        REFAH = '17', _('Refah Bank')
        RESALAT_GHARZOLHASANEH = '18', _('Resalat Gharzolhasaneh Bank')
        SAMAN = '19', _('Saman Bank')
        SARMAYEH = '20', _('Sarmayeh Bank')
        SHAHR = '21', _('Shahr Bank')
        SEPAH = '22', _('Sepah Bank')
        SANAT_AND_MADAN = '23', _('Sanat and Madan Bank')
        SADERAT = '24', _('Saderat Bank')
        SINA = '25', _('Sina Bank')
        TOSEH_TAAVAON = '26', _('Toseh Taavon Bank')
        TEJARAT = '27', _('Tejarat Bank')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banks', verbose_name=_('bank'))
    name = models.CharField(max_length=2, choices=Name.choices, verbose_name=_('Bank Name'))
    account_number = models.CharField(max_length=250, unique=True, verbose_name=_(' Account Number'))
    shaba_number = models.CharField(
        max_length=24,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{24}$', message=_('Invalid Shaba Number'))],
        verbose_name=_('Shaba Number'),
    )
    cart_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[RegexValidator(regex=r'\d{16}$', message=_('Invalid Cart Number'))],
        verbose_name=_('Cart Number'),
    )

    def clean(self):
        if self.name != Bank.Name.RESALAT_GHARZOLHASANEH:
            if not Bank.objects.filter(name=Bank.Name.RESALAT_GHARZOLHASANEH).exists():
                raise Exception(_('Please first create resalat bank data and then try to submit others banks'))

    def delete(self, force_policy=None, **kwargs):
        if self.name == Bank.Name.RESALAT_GHARZOLHASANEH:
            raise Exception(_('You can not delete your resalat bank'))

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')


class AbstractFamily(BaseModel):
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('last name'))
    birth_certificate_id = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_('Birth Certificate id')
    )  # شماره شناسنامه
    national_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        validators=[RegexValidator(regex=r'^[0-9]\d{9}$|^[1-9]\d{10}$', message=_('invalid national id'))],
        verbose_name=_('National id'),
    )
    birthdate = models.DateField(null=True, blank=True, verbose_name=_('Birthday'))
    birthdate_province = OstanField(related_name='%(class)s_birthdate_province')
    birthdate_city = ShahrestanField(related_name='%(class)s_birthdate_cities')
    issue_place = ShahrestanField(related_name='%(class)s_issue_places')
    first_page_certificate_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/first_certificate_image',
        verbose_name='first page certificate image',
    )
    second_page_certificate_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/second_certificate_image',
        verbose_name='second page certificate image',
    )
    third_page_certificate_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/third_certificate_image',
        verbose_name='third page certificate image',
    )
    forth_page_certificate_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/forth_certificate_image',
        verbose_name='forth page certificate image',
    )
    fifth_page_certificate_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/fifth_certificate_image',
        verbose_name='fifth page certificate image',
    )
    front_identify_card_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/front_identify_card_image',
        verbose_name=_('front identify card image'),
    )  # عکس جلو کارت ملی
    back_identify_card_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='personnel/profile/back_identify_card_image',
        verbose_name=_('back identify card image'),
    )  # عکس پشت کارت ملی

    class Meta:
        abstract = True


class Spouse(AbstractFamily):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spouses', verbose_name=_('user'))
    father_name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Father Name'))

    class Meta:
        verbose_name = _('Spouse')
        verbose_name_plural = _('Spouses')


class Child(AbstractFamily):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children', verbose_name=_('user'))

    def clean(self):
        if self.birthdate.year >= 2006:
            if Child.objects.filter(front_identify_card_image__isnull=True, back_identify_card_image__isnull=True):
                raise Exception(_('Please add identify card for your child'))

    class Meta:
        verbose_name = _('Child')
        verbose_name_plural = _('Children')


# TODO (pejman) add choice field of current_cofirmation_step
class Contract(BaseModel):
    class Status(models.TextChoices):  # وضعیت قرارداد
        EMPTY_CHOICE = ('', _('-------'))
        DRAFT = 'D', _('Draft')
        ACTIVE = 'A', _('Active')
        INACTIVE = 'I', _('Inactive')
        ACCEPTED = 'P', _('Accepted')
        REJECTED = 'R', _('REJECTED')

    class CurrentConfirmationStep(models.TextChoices):
        pass

    class Term(models.TextChoices):  # مدت قرارداد
        EMPTY_CHOICE = ('', _('-------'))
        ONE_MONTH = '1', _('One Month')  # یک ماه
        THREE_MONTH = '3', _('Three Month')  # ۳ ماه
        SIX_MONTH = '6', _('Six Month')  # ۶ ماه
        NINE_MONTH = '9', _('Nine Month')  # ۹ ماه
        ONE_YEAR = '12', _('One Year')  # ۱۲ ماه

    class Type(models.TextChoices):  # نوع قرارداد
        EMPTY_CHOICE = ('', _('-------'))
        FULL_TIME = 'F', _('Full Time')
        PART_TIME = 'P', _('Part Time')
        INTERNSHIP = 'I', _('Internship')

    class InsuranceStatus(models.TextChoices):  # وضعیت بیمه
        EMPTY_CHOICE = ('', _('-------'))
        NORMAL = 'N', _('Normal')  # مشمول عادی
        RETIRED = 'R', _('RETIRED')  # بازنشسته
        INSURANCE_EMPLOYER = 'I', _('Insurance Employer')  # معاف بیمه کارفرما
        PREMIUM_INSURANCE = 'P', _('Premium Insurance')  # معاف حق بیمه
        UNEMPLOYMENT_INSURANCE = 'U', _('Unemployment Insurance')  # معاف بیمه بیکاری

    class InsuranceName(models.TextChoices):
        EMPTY_CHOICE = ('', _('-------'))
        TAMIN_EJTEMAEI = 'T', _('Tamin Ejtemaei Organization')
        SALAMAT = 'S', _('Salamat Organization')
        NIROO_MOSALAH = 'N', _('Niroo Mosalah Organization')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts', verbose_name=_('user'))
    personnel_id = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Personnel ID'))
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.DRAFT, verbose_name=_('contract status')
    )
    term = models.CharField(max_length=2, choices=Term.choices, verbose_name=_('contract term'))
    contract_type = models.CharField(max_length=1, choices=Type.choices, verbose_name=_('contract type'))
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))
    money_obligation = models.PositiveIntegerField(verbose_name=_('money obligation'))  # تعهد مالی
    minimum_working_hour = models.IntegerField(verbose_name=_('minimum working hour'), null=True, blank=True)
    insurance_status = models.CharField(
        max_length=1, choices=InsuranceStatus.choices, verbose_name=_('Insurance Status')
    )
    insurance_province = OstanField(related_name='%(class)s_insurance_provinces', verbose_name='insurance province')
    insurance_city = ShahrestanField(related_name='%(class)s_insurance_cities', verbose_name='insurance city')
    insurance_name = models.CharField(max_length=250, choices=InsuranceName.choices, verbose_name=_('Insurance Name'))
    insurance_branch_number = models.CharField(max_length=250, verbose_name=_('Insurance Branch Number'))
    insurance_number = models.CharField(
        max_length=250,
        validators=[RegexValidator(regex=r'\d{10}$', message=_('invalid insurance number'))],
        verbose_name=_('Insurance Number'),
    )

    def __str__(self):
        return 'user:{},personnel_id:{}'.format(self.user, self.personnel_id)

    def clean(self):
        if self.contract_type == self.Type.PART_TIME:
            if self.minimum_working_hour is None:
                raise Exception('Part time contracts must has minimum hours.')
        else:
            if self.minimum_working_hour is not None:
                raise Exception('Do not give minimum working hours.')

    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')


class ContractComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name=_('user'))
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name='contract_comments', verbose_name=_('contract')
    )
    comment = models.TextField(verbose_name=_('comment'))

    class Meta:
        verbose_name = _('contract comment')
        verbose_name_plural = _('contract comments')


class DeleteDemand(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delete_demands', verbose_name=_('user'))
    delete_reason = models.TextField(verbose_name=_('delete_reason'))

    class Meta:
        verbose_name = _('Delete Demand')
        verbose_name_plural = _('Delete Demands')


class UserRole(BaseModel):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('personnel.Role', verbose_name=_('role'), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')


class Role(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('title'), unique=True, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='roles', verbose_name=_('users'), through=UserRole)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class Permission(BaseModel):
    class Codes(models.TextChoices):
        ALL_PERMISSION = '0', _('All Permission')  # تمام دسترسی ها
        VIEW_AND_CHANGE_USERS_DATA = '1', _('View And Change User Data')  # دسترسی مشاهده و تغییر اطلاعات کاربران
        ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA = '2', _(
            'Accept demand for change users data'
        )  # تایید درخواست ویرایش اطلاعات کاربران
        ARCHIVE = '3', _('Archive')  # آرشیوسازی
        DELETE_DEMAND = '4', _('Delete Demand')  # درخواست حذف کاربران
        ACCEPT_DELETE_DEMAND = '5', _('Accept Delete Demand')  # تایید درخواست حذف کاربران

    code = models.CharField(
        choices=Codes.choices,
        verbose_name=_('code'),
        max_length=1,
    )
    role = models.ForeignKey(Role, related_name='permissions', verbose_name=_('role'), on_delete=models.CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
