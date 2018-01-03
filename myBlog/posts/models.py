from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=1)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to='media/',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field"
                              )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    body = models.TextField()

    objects= PostManager()

    def __str__(self):
        return self.title

    def prettyDate(self):
        return self.date.strftime('%b %e %Y')

    def get_absolute_path(self):
        return reverse("posts:detail", kwargs={"post_slug": self.slug})

    class Meta:
        ordering = ["-date", "-id"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
