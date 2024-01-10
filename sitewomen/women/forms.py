from django import forms
from django.core.exceptions import ValidationError
# from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import *

from captcha.fields import CaptchaField


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


# class AddPostForm(forms.Form):
#     """
#     Класс не связанный с моделью.
#     """
#     title = forms.CharField(label='Заголовок',
#                             min_length=5,
#                             max_length=255,
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                             validators=[
#                                 RussianValidator(),
#                             ],
#                             error_messages={
#                                 'min_length': 'Слишком короткий заголовок. Минимум 4 символа!',
#                                 'required': 'Без заголовка никак',
#                             })
#     slug = forms.SlugField(label='URL',
#                            max_length=255,
#                            widget=forms.TextInput(attrs={'class': 'form-input'}),
#                            # validators=[
#                            #     MinLengthValidator(5, message='Минимум 5 символов'),
#                            #     MaxLengthValidator(100, message='Максимум 100 символов')
#                            #]
#                            )
#     content = forms.CharField(label='Текст статьи',
#                               widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
#                               required=False)
#     is_published = forms.BooleanField(label='Статус',
#                                       required=False,
#                                       initial=True)
#     cat = forms.ModelChoiceField(label='Категория',
#                                  queryset=Category.objects.all(),
#                                  empty_label='Категория не выбрана')
#     husband = forms.ModelChoiceField(label='Муж',
#                                      queryset=Husband.objects.all(),
#                                      required=False,
#                                      empty_label='Не замужем')
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')
#         else:
#             return title


class AddPostForm(forms.ModelForm):
    """
    Класс связанный с моделью.
    """

    cat = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(label='Муж', queryset=Husband.objects.all(), required=False,
                                     empty_label='Не замужем')

    class Meta:
        model = Women
        # Выводить все поля
        # fields = '__all__'
        # Выводить те поля, которые будут перечислены в списке
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']

        # Добавить виджеты полям
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

        # Добавить / Поменять название поля
        labels = {
            'slug': 'URL'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов.')
        return title


# class UploadFileForm(forms.Form):
#     """Класс обработки формы загрузки файла"""
#     # Для любого файла
#     file = forms.FileField(label='Файл')
#     # Чисто для фото
#     # photo = forms.ImageField(label='Фото')


class ContactForm(forms.ModelForm):

    captcha = CaptchaField(label='Капча')

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


# class ContactForm(forms.Form):
#     name = forms.CharField(label='Имя', max_length=50)
#     email = forms.EmailField(label='Email')
#     content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
#     captcha = CaptchaField(label='Капча')
