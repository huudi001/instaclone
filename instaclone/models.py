from django.db import models
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt

class Comments(models.Model):
    name = models.CharField(max_length =30)
    comment = HTMLField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def delete_comments(self):
        self.delete()

    def save_comments(self):
        self.save()

    def update_comments(self):
        self.update()

    @classmethod
    def get_comments(cls):
        all_comments= Comments.objects.all()

class Upload(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comments = models.ForeignKey(Comments)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    upload_image = models.ImageField(upload_to='uploads/', blank=True)


    def __str__(self):
        return self.title

    def delete_uploads(self):
        self.delete()

    def save_uploads(self):
        self.save()

    @classmethod
    def get_uploads(cls):
        all_uploads = Upload.objects.all()
        return all_uploads
