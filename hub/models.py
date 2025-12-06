from django.conf import settings
from django.db import models

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "bmp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm", "ogg"}


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
	media = models.FileField(upload_to="posts/media/", blank=True, null=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.title

	@property
	def media_extension(self) -> str | None:
		if not self.media:
			return None
		return (self.media.name.rsplit(".", 1)[-1]).lower()

	@property
	def has_image(self) -> bool:
		return bool(self.media and self.media_extension in IMAGE_EXTENSIONS)

	@property
	def has_video(self) -> bool:
		return bool(self.media and self.media_extension in VIDEO_EXTENSIONS)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="comments",
	)
	text = models.TextField()
	media = models.FileField(upload_to="comments/media/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return f"Comment by {self.author} on {self.post}"

	@property
	def media_extension(self) -> str | None:
		if not self.media:
			return None
		return (self.media.name.rsplit(".", 1)[-1]).lower()

	@property
	def has_image(self) -> bool:
		return bool(self.media and self.media_extension in IMAGE_EXTENSIONS)

	@property
	def has_video(self) -> bool:
		return bool(self.media and self.media_extension in VIDEO_EXTENSIONS)
