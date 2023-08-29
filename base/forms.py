from django.forms import ModelForm, TextInput
from .models import Snippet, Translate, User, Explain
from django.contrib.auth.forms import UserCreationForm

# Creating form based on the db models
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = '__all__'
        exclude = ['author']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'editor'
        })


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class ExplainForm(ModelForm):
    class Meta:
        model = Explain
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'editor',
                'type': 'submit',
                'name': 'explain',
                'value': '{{form.explain}}'
        })


class TranslateForm(ModelForm):
    class Meta:
        model = Translate
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'editor'
        })