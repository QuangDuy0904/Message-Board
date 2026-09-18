from django.urls import path
from .views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogListView,
    BlogUpdateView,
    add_comment,
    post_like_toggle,
)

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_home"),
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/like/", post_like_toggle, name="post_like"),
    path("post/<int:pk>/comment/", add_comment, name="add_comment"),
]