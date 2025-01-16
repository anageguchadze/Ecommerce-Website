from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class SubCategory(models.Model):
    sub_name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.sub_name

    class Meta:
        db_table = 'subcategory'


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'size'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    discount = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    colour = models.CharField(max_length=255, blank=True, null=True)
    size = models.ManyToManyField(Size, related_name='products', blank=True)


    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.final_price = self.price - self.price * (self.discount / 100)
        else:
            self.final_price = self.price

        if self.stock > 0:
            self.is_in_stock = True
        else:
            self.is_in_stock = False
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'


