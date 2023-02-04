from django import forms
from app.models import Product, Version

BANNED_WORDS = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')


class ProductForm(forms.ModelForm):
    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Использовано запрещенное слово')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Использовано запрещенное слово')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'


class VersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Version
        fields = '__all__'
