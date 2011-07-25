from django import forms
from django.utils.translation import ugettext as _
from models import MyPluginModel

''' 
Define your plugin form here.
More info: https://docs.djangoproject.com/en/dev/topics/forms/
'''
class MyPluginForm(forms.ModelForm):
    """ Main form for adding and editing MyPluginModel
        
    """
    required_css_class = 'required'
    name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'required'}))   

    class Meta(object):
        model = MyPluginModel
        exclude = ('external_id')            