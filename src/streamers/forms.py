from django import forms

class StreamerForm(forms.Form):
    name = forms.CharField(label='Streamer name', max_length=120)
    draft = forms.BooleanField(required=False)
    publish = forms.DateField(widget=forms.SelectDateWidget())
