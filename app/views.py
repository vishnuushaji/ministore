from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from .tokens import AccountActivationTokenGenerator, account_activation_token
from .models import Product,BlogPost
from django.views.generic.edit import FormView
from .forms import AddToCartForm, RemoveFromCartForm, UserRegistrationForm, CustomAuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
    PasswordChangeView as AuthPasswordChangeView,
    PasswordResetView as AuthPasswordResetView,
    PasswordResetDoneView as AuthPasswordResetDoneView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
    PasswordResetCompleteView as AuthPasswordResetCompleteView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .tokens import account_activation_token
from .forms import UserRegistrationForm, CustomAuthenticationForm, ContactForm
from .models import Product,  BlogPost,Testimonial, CartItem,Category,CartItem, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin




class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the latest three blog posts from the database
        latest_posts = BlogPost.objects.order_by('-date_published')[:3]
        context['latest_posts'] = latest_posts

        testimonials = Testimonial.objects.all()[:2]
        context['testimonials'] = testimonials

        
        category_one = Category.objects.get(id=1)
        category_one_products = Product.objects.filter(category=category_one)[:3]
        context['category_one_products'] = category_one_products

        # Fetch any 3 products of category object(2)
        category_two = Category.objects.get(id=2)
        category_two_products = Product.objects.filter(category=category_two)[:3]
        context['category_two_products'] = category_two_products

        return context

    


class ShopView(TemplateView):

    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_one = Category.objects.get(id=1)
        category_one_products = Product.objects.filter(category=category_one)[:3]
        context['category_one_products'] = category_one_products

        # Fetch any 3 products of category object(2)
        category_two = Category.objects.get(id=2)
        category_two_products = Product.objects.filter(category=category_two)[:3]
        context['category_two_products'] = category_two_products
        return context  



class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.all()

        for item in cart_items:
            # Calculate the total price for each item
            item.total_price = item.product.price * item.quantity

        context['cart_items'] = cart_items
        return context
class AddToCartView(LoginRequiredMixin, View):
    template_name = 'add_to_cart.html'
    login_url = 'login'  # Specify your login URL

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = AddToCartForm()
        return render(request, self.template_name, {'product': product, 'form': form})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Check if the product is already in the user's cart
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            
            # If the item is already in the cart, update the quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            return redirect('cart')

        return render(request, self.template_name, {'product': product, 'form': form})


class RemoveFromCartView(View):
    def get(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)

        if cart_item.quantity > 1:
            # If the quantity is greater than 1, decrement the quantity
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # If the quantity is 1, remove the entire CartItem
            cart_item.delete()

        return redirect('cart')



class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'
    login_url = reverse_lazy('login') 

    def get_context_data(self, **kwargs):
        # Retrieve all cart items
        cart_items = CartItem.objects.all()

        # Calculate total quantity and total price
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

       
        product_names = [item.product.name for item in cart_items]

        # Pass data to the checkout template
        context = super().get_context_data(**kwargs)
        context['cart_items'] = cart_items
        context['total_quantity'] = total_quantity
        context['total_price'] = total_price
        context['product_names'] = product_names

        return context

    def post(self, request, *args, **kwargs):
        # Additional logic for processing the checkout form
        # For example, you might want to save the order in the database, process payments, etc.

        # Retrieve all cart items
        cart_items = CartItem.objects.all()

        # Calculate total quantity and total price
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_quantity=total_quantity,
            total_price=total_price
        )

        # Create OrderItem instances for each cart item
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total_price=cart_item.product.price * cart_item.quantity
            )

        # Clear the cart after checkout (adjust this based on your actual cart implementation)
        CartItem.objects.all().delete()

        # Redirect to a success page or another relevant page after checkout
        return redirect('thankyou')

class ThankYouView(TemplateView):
    template_name = 'thankyou.html'    

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_activation_email(self.object)
        return HttpResponse('Please check your email to activate your account.')

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),  
        })
        user.email_user(subject, message)


class LoginView(AuthLoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('index'))


class LogoutView(AuthLogoutView):
    next_page = '/'


class PasswordChangeView(AuthPasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')


class PasswordResetView(AuthPasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(AuthPasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(AuthPasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            
            if user is not None:
                user.is_active = False
                user.save()
            return HttpResponse('Activation link is invalid or has expired.')    
        

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

           
            subject = 'Contact Form Submission'
            message_body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nMessage: {message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['noufalmhd112@gmail.com'] 
            send_mail(subject, message_body, from_email, to_email, fail_silently=False)

            return render(request, 'contact_success.html') 
        return self.render_to_response({'form': form})        
    
class BlogView(ListView):
    template_name = 'blog.html' 
    context_object_name = 'latest_posts'
    model = BlogPost
    ordering = ['-date_published']  
    paginate_by = 3    