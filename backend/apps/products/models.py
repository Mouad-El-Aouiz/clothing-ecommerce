from django.db import models
from django.utils.text import slugify
from django.conf import settings  

def product_image_path(instance, filename):
    # Récupérer le slug du produit
    product_slug = instance.product.slug
    
    # Nettoyer le nom du fichier (enlever les chemins existants)
    clean_filename = filename.split('/')[-1]
    
    # Structure: media/products/nom-du-produit/nom_fichier.jpg
    return f"media/products/{product_slug}/{clean_filename}"

    
def category_image_path(instance, filename):
    """Génère le chemin media/categories/{category_slug}/{filename}"""
    category_slug = instance.slug
    clean_filename = filename.split('/')[-1]
    return f"media/categories/{category_slug}/{clean_filename}"

class Category(models.Model):
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('U', 'Unisexe'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to=category_image_path, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('U', 'Unisexe'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    COLOR_CHOICES = [
        ('BLACK', 'Noir'),
        ('WHITE', 'Blanc'),
        ('RED', 'Rouge'),
        ('BLUE', 'Bleu'),
        ('GREEN', 'Vert'),
        ('YELLOW', 'Jaune'),
        ('PINK', 'Rose'),
        ('GRAY', 'Gris'),
        ('NAVY', 'Bleu Marine'),
        ('BROWN', 'Marron'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def final_price(self):
        product_price = self.product.discount_price if self.product.discount_price else self.product.price
        return product_price + self.price_adjustment

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.get_color_display()}"