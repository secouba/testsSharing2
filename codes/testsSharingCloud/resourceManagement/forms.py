from django import forms
from .models import Resource

"""
RESOURCES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)
"""

class signForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=100)
    
    
    
class bookForm(forms.Form):

    """ Remarque: Si j'utilise un constructeur dans cette classe j'obtient des erreurs ??? """
    def setResource():
        """ Cette fonction permet de charger les ressources depuis la BD."""
        L = [('', 'Choose...')]
        #saving all resources into tuple for the bookForm:   
        all_resource_entries = Resource.objects.all()
        for i in all_resource_entries:
            L.append((i.resourceType,i.resourceType))
        return L
        
    RESOURCES = setResource()    
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'salle de réunion'}))
    startDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type':'date'}))
    endDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type':'date'}))
    resource = forms.ChoiceField(choices=RESOURCES)
    