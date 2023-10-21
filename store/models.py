from django.db import models
from django.urls import reverse
from shop.settings import AUTH_USER_MODEL
from django.utils import timezone


"""
Product
- Nom
- Prix
- La quantité en stock
- Description
- Image
"""
class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    desciption = models.TextField(blank=True)
    image = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    # affiche de la touche voir le site dans admin
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})  # retourne l'url  de la page de detail 
    
# Article (Order)
"""
- Utilisateur
- Produit
- Quantite
- Commandé ou non
"""
class Order(models.Model):
# import depuis settings, si on supprime l'utilisateur, les articles seront automatiquement supprimés aussi
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) # lorsqu'on cree un article, au minimun on 1 article
    ordered = models.BooleanField(default=False) # par default l'article ne sera pas commandé
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # le nom du produit auquel est associé cet article et la quantité
        return f"{self.product.name} ({self.quantity})" 

# Panier (Cart)
"""
- Utilisateur
- Articles
- Commandé ou non
- Date de la commande
"""

class Cart(models.Model):
    # un utilisateur ne peut avoir qu'un seul panier
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order) # plusieurs articles peuvent être ajouter à l'interieur du panier


    def __str__(self):
        # afficher le nom d'utilisateur associé au panier
        return self.user.username

    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        
        self.orders.clear()
        super().delete(*args, **kwargs)