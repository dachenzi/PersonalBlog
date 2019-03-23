from django.db import models
from user.models import User


# Create your models here.

class Post(models.Model):
    class Meta:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, null=False)
    postdate = models.DateField(null=False)

    # 作者
    author = models.ForeignKey(User)

    def __repr__(self):
        return '<Post {} {} {} {}>'.format(
            self.pk, self.title, self.postdate, self.author
        )

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = 'content'

    id = models.AutoField(primary_key=True)
    post = models.OneToOneField(Post)
    content = models.TextField(null=False)

    def __repr__(self):
        return '<Content {} {}>'.format(
            self.post, self.content[1:20]
        )

    __str__ = __repr__
