import os
import pathlib
from random import randrange

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from webapp.helpers.telegram import send_telegram_message


class Message(models.Model):
    email = models.EmailField(unique=True)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.email}: {self.content}"


def post_cover_image_path(instance: "Post", filename: str) -> str:
    file_name = pathlib.Path(filename).stem
    file_ext = pathlib.Path(filename).suffix
    random_part = str(randrange(10**8)).zfill(8)
    return (
            pathlib.Path("posts/")
            / slugify(instance.cover_title)
            / pathlib.Path(f"{file_name}_{random_part}{file_ext}")
    )


def block_image_path(instance: "Image", filename: str) -> pathlib.Path:
    file_name = pathlib.Path(filename).stem
    file_ext = pathlib.Path(filename).suffix
    random_part = str(randrange(10**8)).zfill(8)
    return (
        pathlib.Path("posts/")
        / slugify(instance.post.cover_title)
        / pathlib.Path(f"{file_name}_{random_part}{file_ext}")
    )


class Post(models.Model):
    position = models.PositiveIntegerField()
    cover_title = models.CharField(max_length=100)
    cover_description = models.TextField()
    cover_image = models.ImageField(
        upload_to=post_cover_image_path, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-position"]

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.position is None:
                max_position = Post.objects.aggregate(models.Max("position"))[
                    "position__max"
                ]
                self.position = max_position + 1 if max_position is not None else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Title: {self.cover_title} | Position: {self.position}"


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.tag_name


class Image(models.Model):
    image = models.ImageField(upload_to=block_image_path)
    image_size = models.IntegerField()
    image_alignment = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"Image: {self.image} | Size: {self.image_size} | Alignment: {self.image_alignment}"


class Text(models.Model):
    text = models.TextField()
    text_type = models.CharField(max_length=100)
    text_alignment = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Space(models.Model):
    space_number = models.IntegerField()

    def __str__(self):
        return f"Space Number: {self.space_number}"


# Generic content association model
class Block(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="blocks")

    object_id = models.PositiveIntegerField()
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("object_type", "object_id")

    block_position = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["object_type", "object_id"]),
        ]
        ordering = ["post", "block_position"]


@receiver(post_delete, sender=Post)
def delete_post_cover_image(sender, instance, **kwargs):
    """
    Deletes the cover image from storage when the `Post` object is deleted.
    """

    if instance.cover_image and instance.cover_image.name:
        if default_storage.exists(instance.cover_image.name):
            default_storage.delete(instance.cover_image.name)


@receiver(pre_save, sender=Post)
def delete_post_cover_image_on_update(sender, instance, **kwargs):
    """
    Deletes the old cover image from storage when the `Post` object is updated.
    """
    # Check if the object exists in the database (old instance)
    if instance.pk:
        old_instance = get_object_or_404(Post, instance.pk)

        if (
            old_instance.cover_image
            and old_instance.cover_image != instance.cover_image
        ):
            # Delete the old image from the storage (S3)
            if default_storage.exists(old_instance.cover_image.name):
                default_storage.delete(old_instance.cover_image.name)


@receiver(post_delete, sender=Image)
def delete_block_image(sender, instance, **kwargs):
    """
    Deletes the image file from storage when the `Image` object is deleted.
    """
    if instance.image and instance.image.name:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)


@receiver(post_save, sender=Message)
def new_message_created(sender, instance, created, **kwargs):
    """
    Sends a Telegram message when a new `Message` object is created.
    """
    if created:
        send_telegram_message(
            f"⏱️ {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n📧 {instance.email}\n✍ {instance.content}"
        )
