# Importing necessary module and model
from django import forms  # Module for defining forms
from .models import Account  # Importing model for Account

# Form for user registration
class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Attributes:
        password (CharField): Field for entering password.
        confirm_password (CharField): Field for confirming password.
    """

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        """
        Meta class for RegistrationForm.

        Specifies the model and fields to be used in the form.
        """
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        """
        Validates the form data.

        Raises:
            forms.ValidationError: If the passwords do not match.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match.")
