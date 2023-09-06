from django.db import models

class Order(models.Model):
    account = models.ForeignKey('account.accountUser', on_delete=models.CASCADE)
    menu_item = models.ForeignKey('menu.Menuitem', on_delete=models.CASCADE)
    quantity = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    # Add other fields as needed

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    def __str__(self):
        return f"{self.account.username}'s Order: {self.menu_item.name}"


class Cart(models.Model):
    u_id=models.IntegerField()
    f_id=models.IntegerField()
    quantity=models.FloatField()
