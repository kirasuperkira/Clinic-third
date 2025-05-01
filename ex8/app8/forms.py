from django import forms
from .models import Patient, MedicalRecord, PatientDocument
from django.core.validators import FileExtensionValidator

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date',
                  'gender', 'phone', 'email', 'address']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['blood_type', 'allergies']


class PatientDocumentForm(forms.ModelForm):
    confirm_upload = forms.BooleanField(
        required=True,
        label='Подтверждаю корректность документа',
        help_text='Подтвердите загрузку'
    )

    class Meta:
        model = PatientDocument
        fields = ['document_type', 'file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png,.tif'}),
        }

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date',
                  'gender', 'phone', 'email', 'address']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }