from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

class StreamerManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(StreamerManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Streamer(models.Model):
    name = models.CharField(max_length=120)
    get_channel_url = models.URLField()
    get_stream_url = models.URLField()
    logo = models.URLField()
    video_banner = models.URLField()
    profile_banner = models.URLField()
    url = models.URLField()
    views = models.IntegerField()
    followers = models.IntegerField()
    created_at = models.CharField(max_length=120)
    channel_id = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    language = models.CharField(max_length=120)
    broadcaster_language = models.CharField(max_length=120)
    mature = models.BooleanField(default=False)
    partner = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = StreamerManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("streamers:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]
'''
class Stream(models.Model):
    stream_id = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    game = models.CharField(max_length=120)
    viewers = models.IntegerField()
    video_height = models.IntegerField()
    average_fps = models.IntegerField()
    created_at = models.CharField(max_length=120)
    preview_small = models.URLField()
    preview_medium = models.URLField()
    preview_large = models.URLField()
    preview_template = models.URLField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.game

    def get_absolute_url(self):
        return reverse("streams:detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Streams"
        ordering = ["-timestamp", "-updated"]
'''
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Streamer.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{0}-{1}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Streamer)
