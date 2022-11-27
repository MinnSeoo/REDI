import datetime
from django.db import models
from core.models import CustomModelImageField
from django.shortcuts import reverse


class MyPost(models.Model):

    """Post Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="posts", on_delete=models.CASCADE
    )
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("users.User", related_name="likes", blank=True)

    title = models.CharField(max_length=50)
    picture = CustomModelImageField(upload_to="post_pics", blank=True, null=True)

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

    def get_update_date_part(self):
        return self.updated.date()

    def get_update_time_part(self):
        return self.updated.time()

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def get_comments(self):
        return self.comments.order_by("-pk")


class Comment(models.Model):

    """Comment Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        "users.User", related_name="comment_likes", blank=True
    )

    context = models.CharField(max_length=50)

    post = models.ForeignKey(
        "MyPost", related_name="comments", on_delete=models.CASCADE
    )

    def get_likes(self):
        return self.likes.count()
