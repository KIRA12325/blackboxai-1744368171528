from django import forms
from .models import Medicine, Reminder, ScanHistory

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'dosage', 'manufacturer', 'description', 'warnings', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'warnings': forms.Textarea(attrs={'rows': 4}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['medicine', 'doctor', 'start_date', 'end_date', 'frequency', 'time', 'dosage', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['doctor'].queryset = user.doctors.all()

class ScanHistoryForm(forms.ModelForm):
    class Meta:
        model = ScanHistory
        fields = ['medicine', 'image', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
