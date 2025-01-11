from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_set", blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )

    favorites = models.ManyToManyField("Post", related_name="favorited_by", blank=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200, default="Unknown Brand")
    model = models.CharField(max_length=200, default="Unknown Model")
    mileage = models.IntegerField(default=0)
    body_type = models.CharField(max_length=200, default="Unknown Body Type")
    power = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "cars"


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Default Title")
    description = models.TextField(default="Default Description")
    pub_date = models.DateTimeField("date published")
    image = models.ImageField(upload_to="ads/", null=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "ads"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField("date published")
    image = models.ImageField(null=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "posts"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=200, default="Default Comment Text")
    pub_date = models.DateTimeField("date published", default=timezone.now)

    class Meta:
        db_table = "comments"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = "users_favorites"
        managed = False
