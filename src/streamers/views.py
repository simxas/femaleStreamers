from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StreamerForm
from .models import Streamer
import requests
import json
from django.utils import timezone

# showing all currently live streamers
def live_streamers(request):
    today = timezone.now().date()
    queryset_list = Streamer.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Streamer.objects.all()

    live_streams = []
    for streamer in queryset_list:
        url = "https://api.twitch.tv/kraken/streams/{0}".format(streamer.name)
        headers = {"Client-ID": streamer.client_id}
        r = requests.get(url, headers=headers).json()
        if r["stream"] != None:
            live_streams.append(r)

    paginator = Paginator(live_streams, 6)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    print(queryset)
    context = {
        "streamers": queryset,
        "title": "Currently live streams",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "live_streamers.html", context)

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
    headers = {"Client-ID": instance.client_id}
    r = requests.get(url, headers=headers).json()
    # print(r["videos"][0])
    context = {
        "instance": instance,
        "r": r["videos"],
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
        client_id = form.cleaned_data["client_id"]

        url = 'https://api.twitch.tv/kraken/channels/{0}'.format(name)
        headers = {"Client-ID": client_id}
        r = requests.get(url, headers=headers).json()

        streamer = Streamer(
            _id = r["_id"],
            name = r["name"],
            logo = r["logo"],
            video_banner = r["video_banner"],
            profile_banner = r["profile_banner"],
            url = r["url"],
            views = r["views"],
            followers = r["followers"],
            created_at = r["created_at"],
            display_name = r["display_name"],
            language = r["language"],
            broadcaster_language = r["broadcaster_language"],
            mature = r["mature"],
            partner = r["partner"],
            draft = draft,
            publish = publish,
            client_id = client_id
        )
        # TooDo check if streamer already exist and if it is then update it insted of creating new
        streamer.save()

    context = {
        "form": form,
    }
    return render(request, "streamer_form.html", context)
