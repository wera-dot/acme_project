from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Birthday, Congratulation
# from django.forms.widgets import SelectDateWidget
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}

class BirthdayForm(forms.ModelForm):

    class Meta:
         model = Birthday
        #  fields = '__all__'
         exclude = ('author',)

        #  widgets = {
        #     'birthday': SelectDateWidget(
        #          empty_label=("Choose Year", "Choose Month", "Choose Day")
        #     )            
        # }
        
         widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
         }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0] 

    def clean(self):
        # Вызов родительского метода clean.
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )


# class BirthdayForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=20)
#     last_name = forms.CharField(
#         label='Фамилия', required=False, help_text='Необязательное поле'
#     )
#     birthday = forms.DateField(
#         label='Дата рождения',
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )


# IntegerField для целочисленных полей,
# CharField для текстовых полей,
# DateField для полей с датой.


class CongratulationForm(forms.ModelForm):
    
    class Meta:
        model = Congratulation
        fields = ('text',) 