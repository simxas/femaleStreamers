from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StreamerForm
from .models import Streamer
import requests
import json
from django.utils import timezone
from django.conf import settings
import json

# return all the streamers as json objects
def streamers_json(request, id=None):
    queryset_list = Streamer.objects.active()

    # pseudo additional authentication for Nodejs
    if id == "foo":
        queryset_list = Streamer.objects.all()

    data = serializers.serialize('json', queryset_list)

    # for testing:
    # channels = ["OGNGlobal", "OGN_OW", "ESL_Overwatch"]
    channels = []
    for channel in queryset_list:
        channels.append(channel.name)

    json_stuff = json.dumps({"channels" : channels})
    print("=======================")
    print("Received a request")
    print("=======================")
    return HttpResponse(json_stuff, content_type="application/json")

def femalestreamers(request):
    context = {
        "title": "Female Streamers",
    }

    return render(request, "femalestreamers.html", context)

# showing all currently live streamers
def live_streamers(request):
    context = {
        "title": "Currently live streamers",
    }

    return render(request, "live_streamers.html", context)

# showing selected live stream
def stream_detail(request, name):
    print(name)
    url = "https://api.twitch.tv/kraken/streams/{0}".format(name)
    print(url)
    headers = {"Client-ID": settings.CLIENT_ID}
    r = requests.get(url, headers=headers).json()

    context = {
        "title": "Live stream of {0}".format(r["stream"]["channel"]["display_name"]),
        "instance": r,
        "name": name,
    }

    return render(request, "stream_detail.html", context)

# showing all streamers
def streamers_list(request):
    today = timezone.now().date()
    queryset_list = Streamer.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Streamer.objects.all()

    paginator = Paginator(queryset_list, 6)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "streamers": queryset,
        "title": "All streamers aded to this website",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "streamers_list.html", context)

# showing selected streamer details
def streamer_detail(request, slug):
    instance = get_object_or_404(Streamer, slug=slug)

    # getting channel videos
    url = "https://api.twitch.tv/kraken/channels/{0}/videos?limit=3".format(instance.name)
    headers = {"Client-ID": settings.CLIENT_ID}
    r = requests.get(url, headers=headers).json()
    videos = True
    if r["videos"] == []:
        videos = False
    context = {
        "instance": instance,
        "r": r["videos"],
        "videos": videos,
    }
    return render(request, "streamer_detail.html", context)

# creating new streamer
def create_streamer(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = StreamerForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        name = form.cleaned_data["name"]
        draft = form.cleaned_data["draft"]
        publish = form.cleaned_data["publish"]

        url = 'https://api.twitch.tv/kraken/channels/{0}'.format(name)
        headers = {"Client-ID": settings.CLIENT_ID}
        r = requests.get(url, headers=headers).json()

        obj, created = Streamer.objects.update_or_create(
            name=r["name"],
            defaults={
                "_id": r["_id"],
                "name": r["name"],
                "logo": r["logo"],
                "video_banner": r["video_banner"],
                "profile_banner": r["profile_banner"],
                "url": r["url"],
                "views": r["views"],
                "followers": r["followers"],
                "created_at": r["created_at"],
                "display_name": r["display_name"],
                "language": r["language"],
                "broadcaster_language": r["broadcaster_language"],
                "mature": r["mature"],
                "partner": r["partner"],
                "draft": draft,
                "publish": publish,
            },
        )

    context = {
        "form": form,
    }
    return render(request, "streamer_form.html", context)
