import datetime
from django.db import models
from core.models import CustomModelImageField
from django.shortcuts import reverse


class BaseTextModel(models.Model):

    """Base Text Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="posts", on_delete=models.CASCADE
    )
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("users.User", related_name="likes", blank=True)

    def get_likes(self):
        return self.likes.count()

    def get_comment_num(self):
        return self.comments.count()

    def is_today(self):
        return datetime.datetime.now().date() == self.created.date()

    def get_date_part(self):
        return self.created.date()

    def get_time_part(self):
        return self.created.time()


class MyPost(BaseTextModel):

    """Post Model Definition"""

    title = models.CharField(max_length=50)
    picture = CustomModelImageField(upload_to="post_pics", blank=True)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})


class Comment(BaseTextModel):

    """Comment Model Definition"""

    post = models.ForeignKey(
        "MyPost", related_name="comments", on_delete=models.CASCADE
    )
