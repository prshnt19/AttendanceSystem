from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.PasswordInput()
    )

    contact = forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    centre_name = forms.CharField()
    centre_id = forms.CharField()