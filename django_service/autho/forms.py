from django import forms

class PhoneChannelForm(forms.Form):
    # country_code = forms.ChoiceField(
    #     choices=[
    #         ('+7', 'Russia (+7)'),
    #         ('+998', 'Uzbekistan (+998)'),
    #         ('+7', 'Kazakhstan (+7)'),
    #         ('+375', 'Belarus (+375)'),
    #         ('+1', 'United States (+1)'),
    #         ('+86', 'China (+86)'),
    #         ('+91', 'India (+91)'),
    #     ],
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Номер телефона, начиная с кода страны'}
        )
    )
    channel = forms.ChoiceField(
        choices=[
            ('Sms', 'Sms'),
            ('Telegram', 'Telegram'),
            ('Whatsapp', 'Whatsapp'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    bind_url = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )


class PhoneCodeForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Номер телефона, начиная с кода страны'}
        )
    )
    code = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Код'}
        )
    )
    bind_url = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
