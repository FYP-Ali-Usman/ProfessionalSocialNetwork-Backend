from django import forms
from .models import Profile as ProfileModel
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'
    
    def clean_organization(self, *args, **kwargs):
        organization = self.cleaned_data.get('organization')
        if len(organization) > 80:
            raise forms.ValidationError('organization name is too long')
        return organization
    def clean_about(self, *args, **kwargs):
        about = self.cleaned_data.get('about')
        if len(about) > 380:
            raise forms.ValidationError('about details are too long')
        return about