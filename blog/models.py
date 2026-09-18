from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE
  )
  body = models.TextField()
  image = models.ImageField(upload_to="images/", blank=True, null=True)
  audio = models.FileField(upload_to="audios/", blank=True, null=True)
  # Trường lưu danh sách người đã bấm tim
  likes = models.ManyToManyField(
      settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
  )

  def total_likes(self):
    return self.likes.count()

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
  post = models.ForeignKey(
      Post, on_delete=models.CASCADE, related_name="comments"
  )
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  parent = models.ForeignKey(
      "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
  )

  class Meta:
    ordering = ["created_at"]

  def __str__(self):
    return f"{self.author.username}: {self.body[:20]}"

