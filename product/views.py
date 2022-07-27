from django.shortcuts import get_object_or_404, render

from product.models import Product


#  Product Detail view (FBV)
def product(request,slug):
    product = get_object_or_404(Product, slug=slug) # Get object by slug or throw 404

    return render(request, 'product/product.html', {'product': product})

    