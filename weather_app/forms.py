from django.forms import ModelForm, TextInput

from . models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields=['name']
        # this widgets and it's info will be used to take the name of the city
        widgets = {'name':TextInput(attrs={'class':'input','placeholder':'City Name'})}

class CityUpdateForm(ModelForm):
    class Meta:
        model = City
        fields=['name']