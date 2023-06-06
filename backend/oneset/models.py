from django.db import models
from django.contrib.auth.models import AbstractUser

from utility.pcloud import uploadFile, deleteFile

from core.views import getAuth

# ----------All app Users (including Customers)--------------


class User(AbstractUser):
    email = models.EmailField(max_length=50, blank=True, null=True)
    first_name = None
    last_name = None
    phoneNumber = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=80, unique=False)
    isCustomer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = "phoneNumber"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username + ' - ' + self.phoneNumber


# ----------Categories to categorize Event type--------------
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=25)
    link = models.URLField(unique=True)
    thumbnail = models.ImageField(
        upload_to='thumbnail/', blank=True, null=True)
    pcloudFileId = models.CharField(max_length=300, blank=True)
    pubCode = models.CharField(max_length=1000)

    def save(self, *args, **kwargs) -> None:
        if self.thumbnail:
            data = self.thumbnail
            auth = getAuth()
            if auth:
                response = uploadFile(auth=auth,
                                      data=data, folderPath='/category')
            if response != 400:
                self.pcloudFileId = response['fileid']
                self.link = response['publiclink']
                self.pubCode = response['code']
        self.thumbnail = None
        return super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        auth = getAuth()
        if auth:
            response = deleteFile(auth=auth, fileid=self.pcloudFileId)
            if response == 200:
                super(Category, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# ---------------- used to identify the mode of transaction
class PayMode(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# ------------------ these locations are assigned to even to filter them
class Location(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


#  -------------------- these roles are assigned to staff according the event
class Role(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
