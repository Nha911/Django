from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Product, ProductImage
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from django.conf import settings
# views.py (write logic using those models)
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
    from .models import ProductImage
    if request.method == 'POST':
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()
        image_url = request.POST.get('image', '').strip()
        image_file = request.FILES.get('image_file')
        # Remove name, but set a default value to satisfy DB constraint
        product = Product.objects.create(
            name='Product',
            price=price,
            stock=stock
        )
        if image_file:
            product.image = image_file
            product.save()
        if image_url:
            ProductImage.objects.create(product=product, image_url=image_url)
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
        # product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        image_url = request.POST.get('image', '').strip()
        image_file = request.FILES.get('image_file')
        # Only update image if a new file is uploaded
        if image_file:
            product.image = image_file
            product.save()
        # Only add ProductImage if a new URL is provided and not already present
        elif image_url:
            if not ProductImage.objects.filter(product=product, image_url=image_url).exists():
                ProductImage.objects.create(product=product, image_url=image_url)
            product.save()
        # If neither, do not change image fields
        else:
            product.save()
        return redirect('product')

    latest_image_url = product.images.last().image_url if product.images.exists() else ''
    return render(request, 'edit_product.html', {'product': product, 'latest_image_url': latest_image_url})

def Home(request):
    return render(request=request, template_name='home.html')

def product(request):
   
    products = Product.objects.all().order_by('id')
    # Check for missing image files and set image to None if missing
    for p in products:
        if p.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(p.image))
            if not os.path.isfile(image_path):
                p.image = None
        # If no image and at least one ProductImage, set image_url as a fallback attribute
        if not p.image and p.images.exists():
            p.fallback_image_url = p.images.first().image_url
        else:
            p.fallback_image_url = None
    products = list(products)
    return render(request, 'product.html', {'products': products})

def shop_products(request):
    import os
    from django.conf import settings
    products = Product.objects.all().order_by('id')
    for p in products:
        # Check if uploaded image exists
        if p.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(p.image))
            if not os.path.isfile(image_path):
                p.image = None
        # Always try to show up to 4 images: uploaded image, then up to 3 ProductImage URLs
        p.display_images = []
        if p.image:
            p.display_images.append(p.image.url)
        for img in p.images.all()[:4-len(p.display_images)]:
            p.display_images.append(img.image_url)
        # Fill with placeholder if less than 4
        while len(p.display_images) < 4:
            p.display_images.append('https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM=')
    products = list(products)
    return render(request, 'shop_products.html', {'products': products})

def product_table(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'table.html', {'products': products})

def brand(request):
    if request.method == 'POST':
        from .models import Brand
        from django import forms
        class BrandForm(forms.ModelForm):
            class Meta:
                model = Brand
                fields = ['name', 'description']
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand')
    else:
        from .models import Brand
        from django import forms
        class BrandForm(forms.ModelForm):
            class Meta:
                model = Brand
                fields = ['name', 'description']
        form = BrandForm()
    brands = Brand.objects.all().order_by('id')
    return render(request, 'brand.html', {'form': form, 'brands': brands})

def supplier(request):
    if request.method == 'POST':
        from .models import Supplier
        from django import forms
        class SupplierForm(forms.ModelForm):
            class Meta:
                model = Supplier
                fields = ['name', 'address', 'phone_number']
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier')
    else:
        from .models import Supplier
        from django import forms
        class SupplierForm(forms.ModelForm):
            class Meta:
                model = Supplier
                fields = ['name', 'address', 'phone_number']
        form = SupplierForm()
    suppliers = Supplier.objects.all().order_by('id')
    return render(request, 'supplier.html', {'form': form, 'suppliers': suppliers})

def customer(request):
    if request.method == 'POST':
        from .models import Customer
        from django import forms
        class CustomerForm(forms.ModelForm):
            class Meta:
                model = Customer
                fields = ['first_name', 'last_name', 'gender', 'phone_number', 'address']
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')
    else:
        from .models import Customer
        from django import forms
        class CustomerForm(forms.ModelForm):
            class Meta:
                model = Customer
                fields = ['first_name', 'last_name', 'gender', 'phone_number', 'address']
        form = CustomerForm()
    customers = Customer.objects.all().order_by('id')
    return render(request, 'customer.html', {'form': form, 'customers': customers})

def productreview(request):
    if request.method == 'POST':
        from .models import ProductReview
        from django import forms
        class ProductReviewForm(forms.ModelForm):
            class Meta:
                model = ProductReview
                fields = ['barocde', 'name', 'price', 'stock', 'description', 'category_id', 'brand_id', 'product_id']
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productreview')
    else:
        from .models import ProductReview
        from django import forms
        class ProductReviewForm(forms.ModelForm):
            class Meta:
                model = ProductReview
                fields = ['barocde', 'name', 'price', 'stock', 'description', 'category_id', 'brand_id', 'product_id']
        form = ProductReviewForm()
    productreviews = ProductReview.objects.all().order_by('id')
    return render(request, 'productreview.html', {'form': form, 'productreviews': productreviews})

