from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    nickname = forms.CharField(max_length=30, required=True)
    phone_regex = RegexValidator(regex=r'^\d{3}-\d{3,4}-\d{4}$', message="전화번호는 '000-0000-0000' 형식이어야 합니다.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=15, required=True)  # Update phone number field with regex validation

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'nickname', 'phone_number', 'password1', 'password2']

        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']