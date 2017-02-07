from django.shortcuts import render

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
