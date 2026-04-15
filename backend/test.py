from apps.products.models import ProductImage

for img in ProductImage.objects.all():
    if 'media/products/' in img.image.name:
        # Renommer le chemin
        new_name = img.image.name.replace('media/products/', 'products/')
        img.image.name = new_name
        img.save()
        print(f"✅ Migré: {new_name}")