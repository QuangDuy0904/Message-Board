from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Comment, Post
from django.http import JsonResponse
# ==============================
# 1. CÁC CLASS XỬ LÝ BÀI VIẾT (POST)
# ==============================


class BlogListView(ListView):
  """Trang chủ: hiển thị danh sách bài viết."""

  model = Post
  template_name = "home.html"


class BlogDetailView(DetailView):
  """Trang chi tiết: xem bài viết, media, tim và bình luận."""

  model = Post
  template_name = "post_detail.html"


class BlogCreateView(CreateView):
  """Trang tạo bài viết mới."""

  model = Post
  template_name = "post_new.html"
  fields = ["title", "author", "body", "image", "audio"]


class BlogUpdateView(UpdateView):
  """Trang chỉnh sửa bài viết đã có."""

  model = Post
  template_name = "post_edit.html"
  fields = ["title", "body", "image", "audio"]


class BlogDeleteView(DeleteView):
  """Trang xác nhận xóa bài viết."""

  model = Post
  template_name = "post_delete.html"
  success_url = reverse_lazy("blog_home")


# ==============================
# 2. XỬ LÝ TƯƠNG TÁC (TIM & BÌNH LUẬN)
# ==============================


@login_required
def post_like_toggle(request, pk):
  post = get_object_or_404(Post, pk=pk)
  liked = False
  if post.likes.filter(id=request.user.id).exists():
    post.likes.remove(request.user)
  else:
    post.likes.add(request.user)
    liked = True

  # Trả về kết quả JSON để trình duyệt cập nhật tức thì, không cần tải lại trang
  return JsonResponse(
      {
          "liked": liked,
          "total_likes": post.total_likes(),
      }
  )


@login_required
def add_comment(request, pk):
  """Gửi bình luận mới hoặc trả lời bình luận (Reply)."""
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    body = request.POST.get("body", "").strip()
    parent_id = request.POST.get("parent_id")
    if body:
      parent_obj = (
          Comment.objects.filter(id=parent_id).first() if parent_id else None
      )
      Comment.objects.create(
          post=post, author=request.user, body=body, parent=parent_obj
      )
  return redirect("post_detail", pk=pk)