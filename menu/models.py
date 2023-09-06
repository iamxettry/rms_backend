from django.db import models

# Create your models here.


class  Menuitem(models.Model):
    name = models.CharField('Name', max_length=50)
    category=models.CharField('category',max_length=40)
    price = models.DecimalField("Price",max_digits=6, decimal_places=1 )
    itemtype=models.BooleanField(False)
    img=models.ImageField(blank=True,null=True, upload_to='menu-images/')
    available=models.BooleanField(False)
    calorie=models.IntegerField()

    def __str__(self):
        return self.name