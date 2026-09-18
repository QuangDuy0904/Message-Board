from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import UserCreationForm
from .models import User


class SignUpView(SuccessMessageMixin, CreateView):
  """Trang đăng ký tài khoản mới."""

  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"
  success_message = (
      "Đăng ký tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ."
  )


class UserListView(UserPassesTestMixin, ListView):
  """Trang danh sách thành viên - chỉ Admin/Staff mới xem được."""

  model = User
  template_name = "registration/user_list.html"
  context_object_name = "users"

  def test_func(self):
    return self.request.user.is_staff