from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder


class FilterForm(forms.Form):
    protocol = forms.CharField(label="Protocol", max_length=10, required=False)
    mac = forms.CharField(label="MAC", max_length=17, required=False)
    macdst = forms.CharField(label="MACdst", max_length=17, required=False)
    ip = forms.CharField(label="IP", max_length=15, required=False)
    ipdst = forms.CharField(label="IPdst", max_length=15, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'idFilterForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = 'index'
        self.helper.add_input(Submit('submit', 'Filtrar'))


class SignupForm(forms.Form, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup_view'
        self.helper.add_input(Submit('registrar', 'Registrar'))



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )
