import os
import pathlib

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
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
    return (
        pathlib.Path("posts/") / slugify(instance.cover_title) / pathlib.Path(filename)
    )


def block_image_path(instance: "Image", filename: str) -> pathlib.Path:
    return (
        pathlib.Path("posts/")
        / slugify(instance.post.cover_title)
        / pathlib.Path(filename)
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


# @receiver(post_delete, sender=Post)
# def delete_post_cover_image(sender, instance, **kwargs):
#     """
#     Deletes cover image and its folder from filesystem when corresponding `Post` object is deleted.
#     """
#     if instance.cover_image and instance.cover_image.name:
#         image_path = instance.cover_image.path
#         image_dir = os.path.dirname(image_path)
#         if os.path.isfile(image_path):
#             os.remove(image_path)
#         # Remove the directory if it is empty
#         if os.path.isdir(image_dir) and not os.listdir(image_dir):
#             os.rmdir(image_dir)


@receiver(pre_save, sender=Post)
def delete_post_cover_image_on_update(sender, instance, **kwargs):
    """
    Deletes old cover image from filesystem when the `Post` object is updated.
    """
    # Check if the object exists in the database (old instance)
    if instance.pk:
        try:
            old_instance = Post.objects.get(pk=instance.pk)
        except Post.DoesNotExist:
            return

        # Check if the cover image has changed
        if (
            old_instance.cover_image
            and old_instance.cover_image != instance.cover_image
        ):
            old_image_path = old_instance.cover_image.path
            old_image_dir = os.path.dirname(old_image_path)

            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

            # Remove the directory if it is empty
            if os.path.isdir(old_image_dir) and not os.listdir(old_image_dir):
                os.rmdir(old_image_dir)


@receiver(post_delete, sender=Image)
def delete_block_image(sender, instance, **kwargs):
    """
    Deletes post content image and its folder from filesystem when corresponding content object is deleted.
    """
    if instance.image and instance.image.name:
        image_path = instance.image.path
        image_dir = os.path.dirname(image_path)
        if os.path.isfile(image_path):
            os.remove(image_path)
        # Remove the directory if it is empty
        if os.path.isdir(image_dir) and not os.listdir(image_dir):
            os.rmdir(image_dir)


@receiver(post_save, sender=Message)
def new_message_created(sender, instance, created, **kwargs):
    """
    Sends a Telegram message when a new `Message` object is created.
    """
    if created:
        send_telegram_message(
            f"⏱️ {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n📧 {instance.email}\n✍ {instance.content}"
        )
