from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=250)
    date= models.DateTimeField(auto_now=False, auto_now_add=True)
    image= models.ImageField(upload_to='media/')
    body= models.TextField()

    def __str__(self):
        return self.title

    def prettyDate(self):
        return self.date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

    def get_absolute_path(self):
        return reverse("posts:detail",kwargs={"post_id":self.id})

