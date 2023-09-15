from django.db import models

# Create your models here.


class  Menuitem(models.Model):
    VEG = 'VEG'
    NON_VEG = 'NON_VEG'
    NONE = 'NONE'

    TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (NONE, 'None of them'),
    ]
    name = models.CharField('Name', max_length=50)
    category=models.CharField('category',max_length=40)
    price = models.DecimalField("Price",max_digits=6, decimal_places=1 )
    itemtype=models.CharField(max_length=8,
        choices=TYPE_CHOICES,
        default=NONE)
    img=models.ImageField(blank=True,null=True, upload_to='menu-images/')
    available=models.BooleanField(False)
    calorie=models.IntegerField(blank=True)

    def __str__(self):
        return self.name