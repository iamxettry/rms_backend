from django.db import models
from decimal import Decimal
class Order(models.Model):
    account = models.ForeignKey('account.accountUser', on_delete=models.CASCADE)
    menu_item = models.ForeignKey('menu.Menuitem', on_delete=models.CASCADE)
    quantity = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    totalPrice=models.FloatField(blank=True, null=True)
    completed=models.BooleanField(default=False)
    # Add other fields as needed

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    def __str__(self):
        return f"{self.account.username}'s Order: {self.menu_item.name}"

    def save(self, *args, **kwargs):
        # Convert the quantity and price to Decimal
        quantity_decimal = Decimal(str(self.quantity))
        price_decimal = Decimal(str(self.menu_item.price))
        
        # Calculate the total price as a Decimal
        self.totalPrice = quantity_decimal * price_decimal
        super(Order, self).save(*args, **kwargs)

class Cart(models.Model):
    u_id = models.ForeignKey('account.accountUser', on_delete=models.CASCADE)
    f_id = models.ForeignKey('menu.Menuitem', on_delete=models.CASCADE)
    quantity=models.FloatField()
    totalPrice=models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f"{self.u_id.username}'s Order: {self.f_id.name}"
    
    def save(self, *args, **kwargs):
        # Convert the quantity and price to Decimal
        quantity_decimal = Decimal(str(self.quantity))
        price_decimal = Decimal(str(self.f_id.price))
        
        # Calculate the total price as a Decimal
        self.totalPrice = quantity_decimal * price_decimal
        super(Cart, self).save(*args, **kwargs)