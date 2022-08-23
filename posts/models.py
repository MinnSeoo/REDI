from django.db import models
from django.core.validators import MinValueValidator


class BaseTextModel(models.Model):

    """Base Text Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="posts", on_delete=models.CASCADE
    )
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(validators=[MinValueValidator(0)])


class MyPost(BaseTextModel):

    """Post Model Definition"""

    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="uploads/post_pics", blank=True)


class Comment(BaseTextModel):

    """Comment Model Definition"""

    post = models.ForeignKey(
        "MyPost", related_name="comments", on_delete=models.CASCADE
    )
