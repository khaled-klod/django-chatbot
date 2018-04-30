from . import models
from django.forms import ModelForm



class applicationForm(ModelForm):
    class Meta:
        model = models.Application
        fields = '__all__'