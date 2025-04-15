from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Max
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic, View

from webapp.forms import MessageForm
from webapp.models import Message, Post, Text, Block, Image, Space, Tag, Comment


class SuperuserRequiredMixin:
    """Mixin to restrict access to superusers only."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                _("Forbidden: You do not have permission to access this page.")
            )
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredCustomMixin:
    """Mixin to restrict access to logged-in users only."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                _("Forbidden: You do not have permission to access this page.")
            )
        return super().dispatch(request, *args, **kwargs)


class PostListView(generic.ListView):
    model = Post
    template_name = "webapp/index.html"


class PostCreateView(SuperuserRequiredMixin, generic.CreateView):
    model = Post
    fields = ["cover_image", "cover_title", "cover_description"]
    template_name = "webapp/post_create.html"
    success_url = reverse_lazy("webapp:index")


class PostUpdateView(SuperuserRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["cover_image", "cover_title", "cover_description"]
    template_name = "webapp/post_update.html"
    success_url = reverse_lazy("webapp:index")


class PostDeleteView(SuperuserRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("webapp:index")


class PostChangePositionView(SuperuserRequiredMixin, View):
    def post(self, request):
        post_position = request.POST.get("post_position")
        position_direction = request.POST.get("position_direction")

        if not post_position or not position_direction:
            return HttpResponseBadRequest(
                "Both 'post_position' and 'position_direction' are required."
            )

        post = get_object_or_404(Post, position=post_position)

        if position_direction == "left":
            next_post = (
                Post.objects.filter(position__gt=post.position)
                .order_by("position")
                .first()
            )
            if next_post:
                post.position, next_post.position = (
                    next_post.position,
                    post.position,
                )
                post.save()
                next_post.save()

        if position_direction == "right":
            next_post = (
                Post.objects.filter(position__lt=post.position)
                .order_by("-position")
                .first()
            )
            if next_post:
                post.position, next_post.position = (
                    next_post.position,
                    post.position,
                )
                post.save()
                next_post.save()

        return redirect("webapp:index")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "webapp/post_detail.html"


class BlockCreateView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        text = request.POST.get("text")
        image = request.FILES.get("image")
        space = request.POST.get("space_number")

        if text:
            new_object = Text.objects.create(
                text=text,
                text_type=request.POST.get("text_type"),
                text_alignment=request.POST.get("text_alignment"),
            )

        elif image:
            new_object = Image.objects.create(
                image=image,
                image_size=request.POST.get("image_size"),
                image_alignment=request.POST.get("image_alignment"),
                post=post,
            )

        elif space:
            new_object = Space.objects.create(space_number=int(space))

        else:
            return redirect("webapp:post_detail", pk=post.id)

        # Create new block associated with the new object
        object_type = ContentType.objects.get_for_model(new_object)
        max_position = Block.objects.filter(post=post).aggregate(Max("block_position"))
        block_position = (
            max_position["block_position__max"] + 1
            if max_position["block_position__max"]
            else 1
        )

        Block.objects.create(
            post=post,
            object_type=object_type,
            object_id=new_object.id,
            block_position=block_position,
        )

        return redirect("webapp:post_detail", pk=post.id)


class BlockDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        block_id = request.POST.get("block_id")

        if not block_id:
            return HttpResponseBadRequest("Block ID is required.")

        block = get_object_or_404(Block, id=block_id)

        # Delete the content object first
        block.content_object.delete()

        # Delete the Block association
        block.delete()

        return redirect("webapp:post_detail", pk=pk)


class BlockChangePositionView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        block_id = request.POST.get("block_id")
        block_direction = request.POST.get("block_direction")

        if not block_id or not block_direction or not post:
            return HttpResponseBadRequest(
                "Both 'block_id' and 'block_direction' are required."
            )

        block = get_object_or_404(Block, id=block_id)

        if block_direction == "up":
            next_block = (
                Block.objects.filter(post=post, block_position__lt=block.block_position)
                .order_by("-block_position")
                .first()
            )
            if next_block:
                block.block_position, next_block.block_position = (
                    next_block.block_position,
                    block.block_position,
                )
                block.save()
                next_block.save()

        if block_direction == "down":
            next_block = (
                Block.objects.filter(post=post, block_position__gt=block.block_position)
                .order_by("block_position")
                .first()
            )
            if next_block:
                block.block_position, next_block.block_position = (
                    next_block.block_position,
                    block.block_position,
                )
                block.save()
                next_block.save()

        return redirect("webapp:post_detail", pk=pk)


class TagCreateView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        tag_name = request.POST.get("tag_name")
        Tag.objects.create(tag_name=tag_name, post=post)

        return redirect("webapp:post_detail", pk=pk)


class TagDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        tag_id = request.POST.get("tag_id")
        Tag.objects.filter(id=tag_id).delete()

        return redirect("webapp:post_detail", pk=pk)


class CommentCreateView(LoginRequiredCustomMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        current_user = request.user
        comment_content = request.POST.get("comment_content")

        if not comment_content:
            return HttpResponseBadRequest("Comment content is required.")

        Comment.objects.create(post=post, author=current_user, content=comment_content)

        return redirect("webapp:post_detail", pk=pk)


class CommentDeleteView(LoginRequiredCustomMixin, View):
    def post(self, request, pk):
        comment_id = request.POST.get("comment_id")
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return redirect("webapp:post_detail", pk=pk)
        else:
            return HttpResponseForbidden(
                _("You do not have permission to delete this comment.")
            )


class AboutMeView(generic.TemplateView):
    template_name = "webapp/about_me.html"


class ResumeView(generic.RedirectView):
    url = "https://flowcv.com/resume/2ij133mut7p8"


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("webapp:send_message")

    def form_valid(self, form):
        messages.success(self.request, "success")
        return super().form_valid(form)
