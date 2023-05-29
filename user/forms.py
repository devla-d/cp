from django import forms
from account.models import Account


from .models import Packages


GENDER = (
    ("បុរស", "ប្រុស"),
    ("ស្ត្រី", "ស្រី"),
)


class UserUpdateForm(forms.ModelForm):

    country = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "input-form", "placeholder": "ប្រទេស"}
        ),
        label="ប្រទេស",
        required=True,
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "input-form", "placeholder": "ទីក្រុង"}
        ),
        label="ទីក្រុង",
        required=True,
    )
    # state = forms.CharField(
    #     max_length=30,
    #     widget=forms.TextInput(
    #         attrs={
    #             'type': 'text',
    #             'class': 'input-form',
    #             "placeholder":'State'
    #         }
    #     ),
    #     label = 'State',
    #     required=True
    # )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "input-form", "placeholder": "អាសយដ្ឋាន"}
        ),
        label="អាសយដ្ឋាន",
        required=True,
    )

    zipcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "input-form",
                "placeholder": "លេខ​កូដ​តំបន់",
            }
        ),
        label="លេខ​កូដ​តំបន់",
        required=True,
    )
    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDER,
            attrs={
                "class": "browser-default custom-select",
                "class": "input-form",
            },
        ),
        label="ភេទ",
        required=True,
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "tel", "class": "input-form", "placeholder": "លេខទូរសព្ទ"}
        ),
        label="លេខទូរសព្ទ",
        required=True,
    )

    date_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={"type": "text", "class": "input-form"}),
        label="ថ្ងៃខែ​ឆ្នាំ​កំណើត",
        required=True,
    )

    class Meta:
        model = Account
        fields = [
            "country",
            "city",
            "address",
            "zipcode",
            "gender",
            "phone",
            "date_of_birth",
        ]


class PasswordChangeForm(forms.ModelForm):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
                "class": "input-form",
            }
        ),
        label="",
        required=True,
    )
    oldpassword = forms.CharField(
        max_length=30,
        label="លេខសំងាត់​ចាស់",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "លេខសំងាត់​ចាស់",
                "class": "input-form",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=30,
        label="ពាក្យសម្ងាត់​ថ្មី",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "ពាក្យសម្ងាត់​ថ្មី",
                "class": "input-form",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=30,
        label="បញ្ជាក់​លេខសំងាត់​ថ្មី",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "បញ្ជាក់​លេខសំងាត់​ថ្មី",
                "class": "input-form",
            }
        ),
    )

    class Meta:
        model = Account
        fields = ["user_id", "oldpassword", "password1", "password2"]

    def clean(self):
        if self.is_valid():
            user_id = self.cleaned_data["user_id"]
            oldpassword = self.cleaned_data["oldpassword"]
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            user = Account.objects.get(id=user_id)
            if password1 != password2:
                raise forms.ValidationError("ពាក្យសម្ងាត់មិនត្រូវគ្នាទេ។")
            if not user.check_password(oldpassword):
                raise forms.ValidationError("ពាក្យសម្ងាត់ចាស់មិនត្រូវគ្នា។")
