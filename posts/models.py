from django.db import models
from django.core.validators import MinValueValidator
from django.shortcuts import reverse


class BaseTextModel(models.Model):

    """Base Text Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="posts", on_delete=models.CASCADE
    )
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)


class MyPost(BaseTextModel):

    """Post Model Definition"""

    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="post_pics", blank=True)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})


class Comment(BaseTextModel):

    """Comment Model Definition"""

    post = models.ForeignKey(
        "MyPost", related_name="comments", on_delete=models.CASCADE
    )
