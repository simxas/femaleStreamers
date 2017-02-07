from django import forms

class StreamerForm(forms.Form):
    name = forms.CharField(label='Streamer name', max_length=120)
    client_id = forms.CharField(label='Client-ID', max_length=120)
