from django.db import models


# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=250)
    date= models.DateTimeField()
    image= models.ImageField(upload_to='media/')
    body= models.TextField()

    def __str__(self):
        return self.title

    def prettyDate(self):
        return self.date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

