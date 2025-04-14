from django.urls import path

from webapp.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostChangePositionView,
    TagCreateView,
    TagDeleteView,
    BlockCreateView,
    BlockDeleteView,
    BlockChangePositionView,
    AboutMeView,
    ResumeView,
    MessageCreateView,
    CommentCreateView,
    CommentDeleteView,
)

app_name = "webapp"

urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path(
        "post/change-position/",
        PostChangePositionView.as_view(),
        name="post_change_position",
    ),
    path(
        "posts/<int:pk>/content/create/",
        BlockCreateView.as_view(),
        name="block_create",
    ),
    path(
        "posts/<int:pk>/content/delete/",
        BlockDeleteView.as_view(),
        name="block_delete",
    ),
    path(
        "posts/<int:pk>/content/change-position/",
        BlockChangePositionView.as_view(),
        name="block_change_position",
    ),
    path("posts/<int:pk>/tag/create/", TagCreateView.as_view(), name="tag_create"),
    path("posts/<int:pk>/tag/delete/", TagDeleteView.as_view(), name="tag_delete"),
    path(
        "posts/<int:pk>/comment/create/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "posts/<int:pk>/comment/delete/",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path("about", AboutMeView.as_view(), name="about_me"),
    path("resume/", ResumeView.as_view(), name="resume"),
    path("send_message/", MessageCreateView.as_view(), name="send_message"),
]
