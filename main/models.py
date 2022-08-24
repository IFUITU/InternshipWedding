from django.db import models
from config.helpers import UploadTo



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=256, null=True, unique=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Event(TimeStampedModel):
    name = models.CharField(max_length=256, null=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=UploadTo("img/events"), null=True)
    
    def __str__(self):
        return self.name


class EventPlace(TimeStampedModel):
    name = models.CharField(max_length=120, null=True)
    address = models.CharField(max_length=256, null=True)
    image = models.ImageField(upload_to=UploadTo("img/event_places"), null=True)
    active = models.BooleanField(default=True)
    event = models.ManyToManyField('Event', related_name="event")
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Service(TimeStampedModel):
    name = models.CharField(max_length=256, null=True)
    event = models.ManyToManyField('Event')
    price = models.CharField(max_length=30, default="0", null=True)
    image = models.ImageField(upload_to=UploadTo("img/services"))
    video = models.FileField(upload_to="videos/serices", null=True, blank=True)
    desc = models.TextField()

    def __str__(self):
        return self.name


STATUS = (('1', 'Preparing'), ('2', 'Ready'), ('3', 'Done'))

class Order(TimeStampedModel):
    author = models.ForeignKey('client.User', on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey("Event", on_delete=models.SET_NULL, null=True)
    event_place = models.ForeignKey("EventPlace", on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField("Service")
    total_price = models.CharField(max_length=30, null=True)
    date_wedding = models.DateField()
    location_wedding = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS, max_length=10, default='1')


class System_Information(TimeStampedModel):
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.phone


class Gallery(TimeStampedModel):
    img = models.ImageField(upload_to=UploadTo("img/gallery"), null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)


    def __str__(self):
        return self.event.name

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

