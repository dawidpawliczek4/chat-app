from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension

# Create your models here.


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(null=True, blank=True,
                            upload_to=category_icon_upload_path)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='server_category')
    description = models.CharField(max_length=255, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    banner = models.ImageField(upload_to=server_banner_upload_path,
                               null=True, blank=True, validators=[validate_image_file_extension])
    icon = models.ImageField(upload_to=server_icon_upload_path, null=True, blank=True, validators=[
                             validate_icon_image_size, validate_image_file_extension])

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Server, id=self.id)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Server, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def server_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'banner' or field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return f"{self.name}-{self.id}"


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=100, null=True)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channel_server')

    def __str__(self):
        return self.name
