from django.http import HttpResponse
from django.shortcuts import render,redirect
from app.models import Slider,Main_category,Product,Category,Color,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.db.models import Max, Min

from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def home(request):

    slider = Slider.objects.all()
    product = Product.objects.all()
    main_category = Main_category.objects.all()
   
    data = {
        'slider':slider,
        'main_category':main_category,
        'product':product,
    }








    return render (request,'home.html',data)





@login_required(login_url = '/accounts/login/')
def product_detail(request,slug):

    product = Product.objects.filter(slug = slug)


    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect ('error404')    

    data ={
        'product':product,
    }

    return render (request,'product_detail.html',data)





def error404(request):
    return render (request,'error404.html')


def my_account(request):
    return render (request,'account/my_account.html')




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    

        if User.objects.filter(username = username).exists():
            messages.success(request,'Already have it....! = USERNAME')
            return redirect ("login")

        if User.objects.filter(email = email).exists():
            messages.success(request,'Already have it....! = EMAIL')
            return redirect ("login")

        user = User(username = username,email = email)
        user.set_password(password)
        user.save()
        messages.success(request,'Register Successfully')
        
    return redirect ('login')




def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
       
        password = request.POST.get('password')


        user = authenticate(request,username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.success(request,'There was a error plz try again....!')
            return redirect ('login')

    return render (request,'account/my_account.html')



def logout_user(request):
    logout(request,)
    return redirect ('home')




def about(request):
    return render (request,'about.html')


def contact(request):
    return render (request,'contact.html')



def shop(request):
    category = Category.objects.all()

    product = Product.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    else:
        product = Product.objects.all()
		

    color = Color.objects.all()

    ColorID = request.GET.get('colorID')

    if ColorID:
        product = Product.objects.filter(color_name_id=ColorID)

    else:
        product = Product.objects.all()



    data = {
        'category':category,
        'product':product,
        'max_price':max_price,
        'min_price':min_price,
        'FilterPrice':FilterPrice,
        'color':color,

    }




    return render (request,'shop.html',data)















def filter_data(request):
    category = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    all_products = Product.objects.all().order_by('-id').distinct()

    if category:
        all_products = all_products.filter(category__id__in=category)

    if brands:
        all_products = all_products.filter(brand__id__in=brands)

    # Render the product HTML template
    html_content = render_to_string('ajax/product.html', {'product': all_products})

    return JsonResponse({'data': html_content})







# def cart(request):
#     return render (request,'cart/cart.html')








@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    
    cart = request.session.get('cart')
    packing_cost = sum(i.get('packing_cost', 0) for i in cart.values() if i)

    tax = sum(item.get('tax', 0) for item in cart.values())

   
    data = {
        'packing_cost':packing_cost,
        'tax':tax,
    }
    return render(request, 'cart/cart.html',data)



def checkout(request):
    cart = request.session.get('cart', {})
    
    # Calculate the costs
    packing_cost = sum(item.get('packing_cost', 0) for item in cart.values())
    tax = sum(item.get('tax', 0) for item in cart.values())
    cart_total_amount = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart.values())

    # Calculate delivery charges
    delivery_charges = 0 if cart_total_amount > 500 else 60

    # Calculate order total
    order_total = cart_total_amount + packing_cost + tax + delivery_charges

    if request.method == "POST":
        # Get billing information from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Save the order with the calculated totals
        order = Order(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            city=city,
            postal_code=postal_code,
            address=address,
            subtotal=cart_total_amount,
            packing_cost=packing_cost,
            tax=tax,
            order_total=order_total
        )
        order.save()

        return redirect('order_success')

    # Prepare data to be sent to the template
    data = {
        'cart_total_amount': cart_total_amount,
        'packing_cost': packing_cost,
        'tax': tax,
        'delivery_charges': delivery_charges,
        'order_total': order_total,
    }

    return render(request, 'checkout.html', data)



def order_success(request):
    return render (request,'order_success.html')








