from django import forms
from models import Lab

class SpeciesForm(forms.Form):
    
    labs = forms.ModelChoiceField(queryset=Lab.objects.all())
    spefile = forms.FileField(label='Select a species.')
