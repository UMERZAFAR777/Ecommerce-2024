from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User,Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from app.models import Order,Product

from django.db.models import Sum






def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/admin/dashboard/')
        
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Debugging: Print username and password
            print(f"Attempting to log in with Username: {username}, Password: {password}")
            
            user = authenticate(request, username=username, password=password)

            # Debugging: Check if user is authenticated
            if user:
                print(f"Authenticated User: {user.username}, Superuser: {user.is_superuser}")
            
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/admin/dashboard/')
            else:
                if user is None:
                    messages.error(request, 'Invalid username or password.')
                else:
                    messages.error(request, 'Sorry, you are not an admin.')
                    
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    
        return render(request, 'custom/login.html')
    
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred during login. Please try again later.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'custom/dashboard.html')







from django.contrib.auth.decorators import login_required, user_passes_test

from django.urls import reverse
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be an admin to view this page.')
        return redirect(reverse('admin_login'))
    


    total_sales = Order.objects.aggregate(total_sales=Sum('order_total'))['total_sales'] or 0

    user = User.objects.all()
    order = Order.objects.all()

    product = Product.objects.all()
    data = {
        'user':user,
        'order':order,
        'product':product,
        'total_sales':total_sales,
    }


    return render(request, 'custom/dashboard.html',data)



def logout_admin(request):
    logout(request,)
    messages.success(request,'Logged Out......!')

    return redirect ('home')



def product_admin(request):
    product = Product.objects.all()
    data = {
        'product':product,
    }
    return render (request,'custom/product.html',data)



def user_admin(request):
    user = User.objects.all()
    data = {
        'user':user,
    }
    return render (request,'custom/user.html',data)


def group_admin(request):
    group = Group.objects.all()
    data = {
        'group':group,
    }
    return render (request,'custom/group.html',data)



from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages



# def update_order_status(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     new_status = request.POST.get('status')
    
#     if new_status:
#         order.status = new_status
#         order.save()

#         # Sending email based on the status
#         if new_status == 'Pending':
#             subject = "Order Delayed"
#             message = "Your package is delayed due to some reason."
#         elif new_status == 'Complete':
#             subject = "Order Shipped"
#             message = "Now your package is transferred."

#         if new_status in ['Pending', 'Complete']:
#             send_mail(subject, message, 'umerzafar433@gmail.com', [order.email])
#             messages.success(request, f"Email sent to {order.email} regarding the status '{new_status}'.")

#     return redirect('/dashboard/')




from django.core.mail import send_mail, BadHeaderError


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status:
        order.status = new_status
        order.save()

        if new_status == 'Pending':
            subject = "Order Delayed"
            message = "Your package is delayed due to some reason."
        elif new_status == 'Complete':
            subject = "Order Shipped"
            message = "Now your package is transferred."

        if new_status in ['Pending', 'Complete']:
            try:
                send_mail(subject, message, 'umerzafar433@gmail.com', [order.email])
                messages.success(request, f"Email sent to {order.email} regarding the status '{new_status}'.")
                print("Email sent successfully")
            except BadHeaderError:
                print("Bad Header Error - Invalid header found.")
                return HttpResponse('Invalid header found.')
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "There was an error sending the email. Please try again later.")
                return HttpResponse(f"There was an error sending the email: {e}")
        else:
            print("No email sent as the status was neither 'Pending' nor 'Complete'.")
    else:
        print("No status provided.")

    return redirect('/admin/dashboard/')


