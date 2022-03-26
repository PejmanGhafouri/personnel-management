from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext as _
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Profile, Spouse, Child, Bank, Education, Contract, Role, Permission, ContractComment
from ..iranian_cities.fields import OstanField, ShahrestanField

User = get_user_model()


class UserForm(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    national_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('1234567890')}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('+989123456789')}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': _('example@example.com')}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'national_id', 'phone_number', 'email')


class ProfileForm(ModelForm):
    gender = forms.ChoiceField(choices=Profile.Gender.choices, widget=forms.RadioSelect)
    father_name = forms.CharField(required=True)
    birth_certificate_id = forms.CharField(required=True)
    birthdate = JalaliDateField(widget=AdminJalaliDateWidget)
    birthdate_province = OstanField()
    birthdate_city = ShahrestanField()
    issue_place = ShahrestanField()
    first_page_certificate_image = forms.ImageField(required=True, widget=forms.FileInput)
    second_page_certificate_image = forms.ImageField(required=True, widget=forms.FileInput)
    third_page_certificate_image = forms.ImageField(required=True, widget=forms.FileInput)
    forth_page_certificate_image = forms.ImageField(required=True, widget=forms.FileInput)
    fifth_page_certificate_image = forms.ImageField(required=True, widget=forms.FileInput)
    front_identify_card_image = forms.ImageField(required=True, widget=forms.FileInput)
    back_identify_card_image = forms.ImageField(required=True, widget=forms.FileInput)
    military_service_status = forms.ChoiceField(
        required=True, choices=Profile.MilitaryServiceStatus.choices, widget=forms.RadioSelect
    )
    military_service_image = forms.ImageField(required=True, widget=forms.FileInput)
    province = OstanField()
    city = ShahrestanField()
    address = forms.CharField(required=True)
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('1234567890')}),
        required=True,
        validators=[RegexValidator(regex=r'^[0-9]{10}$', message=_('invalid postal code'))],
    )
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('02123456789')}),
        required=True,
        validators=[RegexValidator(regex=r'^0[0-9]{2,}[0-9]{7,}$', message=_('invalid telephone'))],
    )
    emergency_telephone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('02123456789')}),
        required=True,
        validators=[RegexValidator(regex=r'^0[0-9]{2,}[0-9]{7,}$', message=_('invalid emergency telephone'))],
    )
    martial_status = forms.ChoiceField(required=True, choices=Profile.MartialStatus.choices)

    class Meta:
        model = Profile
        fields = (
            'gender',
            'father_name',
            'birth_certificate_id',
            'birthdate',
            'birthdate_province',
            'birthdate_city',
            'issue_place',
            'first_page_certificate_image',
            'second_page_certificate_image',
            'third_page_certificate_image',
            'forth_page_certificate_image',
            'fifth_page_certificate_image',
            'front_identify_card_image',
            'back_identify_card_image',
            'military_service_status',
            'military_service_image',
            'province',
            'city',
            'address',
            'postal_code',
            'telephone',
            'emergency_telephone',
            'martial_status',
        )


class EducationForm(ModelForm):
    level = forms.ChoiceField(choices=Education.Level.choices)
    field = forms.ChoiceField(choices=Education.StudyField.choices, widget=forms.Select)
    graduation_date = forms.CharField(widget=forms.DateInput(attrs={'placeholder': '1400'}))
    graduation_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Education
        fields = ('level', 'field', 'graduation_date', 'graduation_image')


class SpouseForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    father_name = forms.CharField()
    national_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('1234567890')}))
    birth_certificate_id = forms.CharField()
    birthdate = JalaliDateField(widget=AdminJalaliDateWidget)
    birthdate_province = OstanField()
    birthdate_city = ShahrestanField()
    issue_place = ShahrestanField()
    first_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    second_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    third_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    forth_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    fifth_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    front_identify_card_image = forms.ImageField(widget=forms.FileInput)
    back_identify_card_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Spouse
        fields = (
            'first_name',
            'last_name',
            'father_name',
            'birth_certificate_id',
            'national_id',
            'birthdate',
            'birthdate_province',
            'birthdate_city',
            'issue_place',
            'first_page_certificate_image',
            'second_page_certificate_image',
            'third_page_certificate_image',
            'forth_page_certificate_image',
            'fifth_page_certificate_image',
            'front_identify_card_image',
            'back_identify_card_image',
        )


class ChildForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    national_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('1234567890')}))
    birth_certificate_id = forms.CharField()
    birthdate = JalaliDateField(widget=AdminJalaliDateWidget)
    birthdate_province = OstanField()
    birthdate_city = ShahrestanField()
    issue_place = ShahrestanField()
    first_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    second_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    third_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    forth_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    fifth_page_certificate_image = forms.ImageField(widget=forms.FileInput)
    front_identify_card_image = forms.ImageField(widget=forms.FileInput)
    back_identify_card_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Child
        fields = (
            'first_name',
            'last_name',
            'birth_certificate_id',
            'national_id',
            'birthdate',
            'birthdate_province',
            'birthdate_city',
            'issue_place',
            'first_page_certificate_image',
            'second_page_certificate_image',
            'third_page_certificate_image',
            'forth_page_certificate_image',
            'fifth_page_certificate_image',
            'front_identify_card_image',
            'back_identify_card_image',
        )


class BankForm(ModelForm):
    name = forms.ChoiceField(choices=Bank.Name.choices, widget=forms.Select)
    account_number = forms.CharField()
    shaba_number = forms.CharField(
        widget=forms.TextInput,
        validators=[RegexValidator(regex=r'^\d{24}$', message=_('Invalid Shaba Number'))],
    )
    cart_number = forms.CharField(validators=[RegexValidator(regex=r'\d{16}$', message=_('Invalid Cart Number'))])

    class Meta:
        model = Bank
        fields = ('name', 'account_number', 'shaba_number', 'cart_number')


ProfileInlineFormset = inlineformset_factory(User, Profile, form=ProfileForm, extra=1)
BankInlineFormset = inlineformset_factory(User, Bank, form=BankForm, extra=1)
EducationInlineFormset = inlineformset_factory(User, Education, form=EducationForm, extra=1)
SpouseInlineFormset = inlineformset_factory(User, Spouse, form=SpouseForm, extra=1)
ChildInlineFormset = inlineformset_factory(User, Child, form=ChildForm, extra=1)


# TODO (pejman) how get list of the user that demand_status is Accepted
class ContractForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select)
    personnel_id = forms.CharField(required=True)
    status = forms.ChoiceField(choices=Contract.Status.choices)
    term = forms.ChoiceField(choices=Contract.Term.choices)
    contract_type = forms.ChoiceField(choices=Contract.Type.choices)
    start_date = JalaliDateField(widget=AdminJalaliDateWidget)
    end_date = JalaliDateField(widget=AdminJalaliDateWidget)
    money_obligation = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Rial'}))
    minimum_working_hour = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'placeholder': 'this field is required if contract type is part time'}),
    )
    insurance_status = forms.ChoiceField(choices=Contract.InsuranceStatus.choices)
    insurance_province = OstanField()
    insurance_city = ShahrestanField()
    insurance_name = forms.ChoiceField(choices=Contract.InsuranceName.choices)
    insurance_branch_number = forms.CharField(required=True)
    insurance_number = forms.CharField(
        required=True, validators=[RegexValidator(regex=r'\d{10}$', message=_('invalid insurance number'))]
    )

    class Meta:
        model = Contract
        fields = (
            'user',
            'personnel_id',
            'status',
            'term',
            'contract_type',
            'start_date',
            'end_date',
            'money_obligation',
            'minimum_working_hour',
            'insurance_status',
            'insurance_province',
            'insurance_city',
            'insurance_name',
            'insurance_branch_number',
            'insurance_number',
        )


class ContractCommentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select)
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), widget=forms.Select)
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContractComment
        fields = ('user', 'contract', 'comment')


class RoleForm(forms.Form):
    title = forms.CharField(
        required=True, max_length=250, widget=forms.TextInput(attrs={'placeholder': _('please choose title for role')})
    )
    codes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True,
        choices=Permission.Codes.choices,
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        if Role.objects.filter(title=title).exists():
            raise ValidationError(_('Duplicate title'))
        return title

    def clean_codes(self):
        codes = self.cleaned_data['codes']
        if len(codes) < 1:
            raise ValidationError('At least select one permission')
        return codes


# TODO (pejman) make field unchangeable and just show the name
class AssignRoleForm(forms.Form):
    role_titles = forms.ModelChoiceField(widget=forms.Select, queryset=Role.objects.all())
    users = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all())
