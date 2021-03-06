from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.utils.text import slugify
import uuid
# import uuid
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    #snippet = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    header_image =  models.ImageField(null=True, blank=True, upload_to='images/')
    content = models.TextField(default="")
    # content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    post_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    likes = models.ManyToManyField(User, related_name='blogs')

    class Meta:
        ordering = ['-created_on']

    def get_total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + "-" + self.post_id.urn

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, default="This user has not written anything here.")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile', default=None)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def __str__(self):
        return str(self.user)