from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class SubCategory(models.Model):
    sub_name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True, upload_to='subcategories_icons')
    

    def __str__(self):
        return self.sub_name

    class Meta:
        db_table = 'subcategory'


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'color'

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
    color = models.ManyToManyField(Color, related_name='products', blank=True)
    size = models.ManyToManyField(Size, related_name='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    

    def update_average_rating(self):
        ratings = self.ratings.all()
        total_ratings = ratings.count()
        self.average_rating = sum(rating.rating for rating in ratings) / total_ratings if total_ratings > 0 else 0
        self.save()


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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.TextField() 
    
    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        db_table = 'product_image'

class ImageSlider(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    image = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'image_slider'


class ProductRating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    session_id = models.CharField(max_length=255, null=True, blank=True) 
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user', 'session_id')  
        db_table = 'product_rating'