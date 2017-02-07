from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .forms import StreamerForm
from .models import Streamer
import requests

def live_streamers(request):

    context = {
        "streamers": 'streamers',
    }

    return render(request, "live_streamers.html", context)

def streamer_detail(request, slug):

    context = {
        "streamer": 'streamer',
    }

    return render(request, "streamer_detail.html", context)

def create_streamer(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = StreamerForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        client_id = form.cleaned_data['client_id']

        url = 'https://api.twitch.tv/kraken/channels/{0}'.format(name)
        headers = {'Client-ID': client_id}
        r = requests.get(url, headers=headers)
        print(r.text)

    context = {
        "form": form,
    }
    return render(request, "streamer_form.html", context)
