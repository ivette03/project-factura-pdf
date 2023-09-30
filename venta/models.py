from django.db import models
from datetime import date
# CLIENTE
class Client(models.Model):
    client_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    identy = models.CharField(max_length=10)
    number_phone= models.CharField(max_length=10)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = "client"
        verbose_name = "client"
        verbose_name_plural = "clients"
    def __str__(self):
        return '{}'.format(self.client_name + " " + self.last_name)
#PROVEEDOR
class Vendor(models.Model):
    vendor_name=models.CharField(max_length=200)
    address=models.CharField(max_length=205)
    number_phone=models.CharField(max_length=10)
    email=models.EmailField()
    class Meta:
        db_table="vendor"
        verbose_name="the vendor"
        verbose_name_plural="vendors"
    def __str__(self):
        return self.vendor_name
#CATEGORIA
class Category(models.Model):
    name=models.CharField(max_length=50)
    class Meta:
        db_table="category"
        verbose_name="category"
        verbose_name_plural="categories"
    def __str__(self):
        return self.name
# PRODUCTO
class Product(models.Model): 
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default='category')
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,default='vendor')
    stock=models.IntegerField(default=1,verbose_name="stock")
    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
    def __str__(self):
        return self.product_name

# FACTURA
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=10, unique=True)
    date = models.DateField(default=date.today)
    client= models.ForeignKey(Client, on_delete=models.CASCADE,default="elige")
    product = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente}"

#OFERTA
class Offer(models.Model):
    offer_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table="offer"
        verbose_name="offer"
        verbose_name_plural="offers"
    def __str__(self):
        return f"Offer: {self.offer_name}"