from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientEditForm, PatientForm, MedicalRecordForm, PatientDocumentForm
from .models import Patient, MedicalRecord, PatientDocument

def patient_list(request):
    patients = Patient.objects.filter(removed=False)
    return render(request, 'patient_list.html', {'patients': patients})


def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        medical_record_form = MedicalRecordForm(request.POST)
        patient_document_form = PatientDocumentForm(request.POST, request.FILES)

        if all([
            patient_form.is_valid(),
            medical_record_form.is_valid(),
            patient_document_form.is_valid()
        ]):
            patient = patient_form.save()

            medical_record = medical_record_form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()

            patient_document = patient_document_form.save(commit=False)
            patient_document.patient = patient
            patient_document.save()

            return redirect('patient_detail', patient_id=patient.id)

    else:
        patient_form = PatientForm()
        medical_record_form = MedicalRecordForm()
        patient_document_form = PatientDocumentForm()

    return render(request, 'add_patient.html', {
        'patient_form': patient_form,
        'medical_record_form': medical_record_form,
        'patient_document_form': patient_document_form
    })

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, removed=False)
    medical_record = MedicalRecord.objects.get(patient=patient)
    documents = PatientDocument.objects.filter(patient=patient)
    return render(request, 'patient_detail.html', {
        'patient': patient,
        'medical_record': medical_record,
        'documents': documents,
    })

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, removed=False)
    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientEditForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, removed=False)
    if request.method == 'POST':
        patient.removed = True
        patient.save()
        return redirect('patient_list')
    return render(request, 'confirm_delete.html', {'patient': patient})