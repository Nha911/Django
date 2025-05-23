from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Product, ProductImage

def about(request):
    return render(request=request, template_name='about.html')

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Category.objects.create(name=name, description=description)
        return redirect('category')
    return render(request, 'add_category.html')

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        Product.objects.create(
            name=name,
            description=description,
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
        category.description = request.POST.get('description', category.description)
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
        # Main image (for online URL or local file)
        image_url = request.POST.get('image', '').strip()
        if image_url:
            # If using ImageField, clear it if a URL is provided
            product.image = None
            product.save()
            # Save as ProductImage if not already present
            if not ProductImage.objects.filter(product=product, image_url=image_url).exists():
                ProductImage.objects.create(product=product, image_url=image_url)
        else:
            product.save()
        # Handle extra images (comma separated URLs)
        extra_images = request.POST.get('extra_images', '')
        if extra_images:
            urls = [url.strip() for url in extra_images.split(',') if url.strip()]
            for url in urls:
                if not ProductImage.objects.filter(product=product, image_url=url).exists():
                    ProductImage.objects.create(product=product, image_url=url)
        return redirect('product')

    return render(request, 'edit_product.html', {'product': product})

def Home(request):
    return render(request=request, template_name='home.html')

def product(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'product.html', {'products': products})

