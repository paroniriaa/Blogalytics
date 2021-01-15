from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
# import uuid
# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    post_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + "-" + self.post_id

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})