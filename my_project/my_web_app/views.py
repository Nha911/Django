from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Product, ProductImage
from django.contrib.auth.decorators import login_required, user_passes_test

# views.py (write logic using those models)

def about(request):
    return render(request=request, template_name='about.html')

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('category')
    return render(request, 'add_category.html')


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )
        return redirect('product')
    return render(request, 'add_product.html')

def admin(request):
    return redirect('/admin/')

def category(request):
    categories = Category.objects.all().order_by('id')
    return render(request, 'category.html', {'categories': categories})

def contact(request):
    return render(request=request, template_name='contact.html')

def delete_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return HttpResponse("Category not found", status=404)
    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return render(request, 'delete_category.html', {'category': category})

def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        product.delete()
        return redirect('product')

    return render(request, 'delete_product.html', {'product': product})

def edit_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return HttpResponse("Category not found", status=404)

    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.save()
        return redirect('category')

    return render(request, 'edit_category.html', {'category': category})

def edit_product(request, product_id):
    from .models import ProductImage
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        image_url = request.POST.get('image', '').strip()
        image_file = request.FILES.get('image_file')
        saved = False
        if image_file:
            product.image = image_file
            product.save()
            saved = True
        if image_url:
            # Only add ProductImage if the URL is valid and not already present
            if not ProductImage.objects.filter(product=product, image_url=image_url).exists():
                ProductImage.objects.create(product=product, image_url=image_url)
            saved = True
        if not saved:
            product.save()
        return redirect('product')

    # Pre-fill the image URL field with the latest ProductImage if it exists
    latest_image_url = product.images.last().image_url if product.images.exists() else ''
    return render(request, 'edit_product.html', {'product': product, 'latest_image_url': latest_image_url})

def Home(request):
    return render(request=request, template_name='home.html')

def product(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'product.html', {'products': products})

