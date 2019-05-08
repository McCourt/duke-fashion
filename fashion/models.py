from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    collegeid = models.IntegerField(default=0)
    username = models.CharField(max_length=256, default="")
    phone = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    email = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.username

class Clothes(models.Model):
    sellerid = models.ForeignKey(Person, on_delete=models.CASCADE)
    orginalprice = models.DecimalField(max_digits=10, decimal_places=2)
    sellprice = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=256)
    brand = models.CharField(max_length=256)
    ctype = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images', default='images/dukeshirt.png')
    details = models.CharField(max_length=256, null=True)
    closed = models.BooleanField()
    openuntil = models.DateTimeField()

    def __str__(self):
        return self.brand + " " + self.ctype


class Bidding(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    biddingprice = models.DecimalField(max_digits=10, decimal_places=2)
    # closed = models.BooleanField(default=False)
    # openuntil = models.DateTimeField()
    biddingtime = models.DateTimeField()

    def __str__(self):
        return self.person.username + " " + self.clothes.__str__()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Person.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
