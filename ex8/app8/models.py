from django.db import models
from django.core.validators import FileExtensionValidator

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    removed = models.BooleanField(default=False, verbose_name='Удален')
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_record')
    blood_type = models.CharField(max_length=3, blank=True, verbose_name='Группа крови')
    allergies = models.TextField(blank=True, verbose_name='Аллергии')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    def __str__(self):
        return f"Медцинская карта {self.patient}"


class PatientDocument(models.Model):
    DOCUMENT_TYPES = [
        ('PASSPORT', 'Паспорт'),
        ('POLICY', 'Медицинский полис'),
        ('SNILS', 'СНИЛС'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name='Тип документа')
    file = models.FileField(
        upload_to='patient_documents/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'tif'])],
        verbose_name='Файл документа'
    )
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f"{self.get_document_type_display()} {self.patient}"