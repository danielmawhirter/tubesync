from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Source, Media
from .tasks import delete_index_source_task, index_source_task, download_media_thumbnail


@receiver(post_save, sender=Source)
def source_post_save(sender, instance, created, **kwargs):
    # Triggered when a source is saved
    if created:
        # If the source is newly created schedule its indexing
        index_source_task(str(instance.pk), repeat=settings.INDEX_SOURCE_EVERY)


@receiver(post_delete, sender=Source)
def source_post_delete(sender, instance, **kwargs):
    # Triggered when a source is deleted
    delete_index_source_task(str(instance.pk))


@receiver(post_save, sender=Media)
def media_post_save(sender, instance, created, **kwargs):
    # Triggered when media is saved
    if created:
        # If the media is newly created fire a task off to download its thumbnail
        metadata = instance.loaded_metadata
        thumbnail_url = metadata.get('thumbnail', '')
        if thumbnail_url:
            download_media_thumbnail(str(instance.pk), thumbnail_url)


@receiver(post_delete, sender=Media)
def media_post_delete(sender, instance, **kwargs):
    # Triggered when media is deleted
    pass
    # TODO: delete thumbnail and media file from disk