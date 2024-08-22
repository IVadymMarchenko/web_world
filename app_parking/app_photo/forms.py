from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, ImageField, TextInput, FileInput, FileField

from .models import Car_Image


def validate_file_size(value):
    
    max_size = 10 * 1024 * 1024  # 10 МБ

    if value.size > max_size:
        raise ValidationError(f"Максимальный размер файла - 10 МБ. Ваш файл слишком большой ({value.size} байт).")



class FormPicture(ModelForm):
    image = FileField(widget=FileInput(attrs={'class':'form-control', 'id':'formFile'}),validators=[validate_file_size])


    class Meta:
        model = Car_Image
        fields = ['image']