from django.conf import settings
from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=150, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	categories = models.ManyToManyField(Category, related_name="posts", blank=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="comments",
	)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return f"Comment by {self.author} on {self.post}"
