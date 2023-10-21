from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Cart, Order
from django.urls import reverse
# Create your views here.

# afficher la page d'accueil
def index(request):
    products = Product.objects.all()
    return render(request, "store/index.html", context={"products": products})

# afficher la page de detail
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product":product})

"""
- user n'a pas encore de panier et veut creer un panier en ajoutant des articles dans son panier
- user a un panier et l'article existe déja dans son panier
"""
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug = slug) # recuperer le produit si il existe
    cart, _ = Cart.objects.get_or_create(user=user) # recuperer le panier associé à l'utilisateur
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)
    # incremente le nombre d'article si l'article est deja dans le panier sinon cree un nouveau panier
    if created: # si l'article n'existe pas
        cart.orders.add(order)
        cart.save() # enregistrer le panier
    else: # si l'article existe increment sa quantité
        order.quantity += 1 
        order.save()
    
    return redirect(reverse("product", kwargs={"slug":slug}))


def cart(request):
    cart=get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"orders":cart.orders.all()}) # passer tous les articles qui sont dans le panier


def delete_cart(request):
    if cart:= request.user.cart: # si le panier existe
        """cart = request.user.cart
        if cart: """ # si le panier existe
    # cart.orders.all().delete() # supprimer le contenu du panier
    cart.delete() # supprimer le panier
    return redirect('index')