from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # para comprobar el intervalo de fechas

# from django.forms import ModelForm
from .models import BookInstance



class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text='Entre una fecha entre hoy y cuatro semanas(por defecto 3).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # La fecha de comprobación no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # La fecha de comprobación está dentro del rango que el bibliotecario puede cambiar (+4 semanas).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_(
                'Invalid date - renewal more than 4 weeks ahead'))

        # Recuerda devolver siempre los datos depurados.
        return data


# from django.forms import ModelForm

# class RenewBookModelForm(ModelForm):
    
#     def clean_due_back(self):
#         data = self.cleaned_data['due_back']

#         # La fecha de comprobación no está en el pasado.
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renowal in past'))

#         # La fecha de comprobación está dentro del rango que el bibliotecario puede cambiar (+4 semanas).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_(
#                 'Invalid date - renowal more than 4 weeks ahead'))

#         # Recuerda devolver siempre los datos depurados.
#         return data

#     class Meta:
#         model = BookInstance
#         fields = ['due_back',]
#         labels = {'due_back': _('Renewal date'),}
#         help_texts = {'due_back': _('Enter a date between now and 4 weeks(default 3.)'),}



    