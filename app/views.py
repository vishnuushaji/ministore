from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from .tokens import AccountActivationTokenGenerator, account_activation_token
from .models import Product, Smartphone, Smartwatch,BlogPost
from django.views.generic.edit import FormView
from .forms import RemoveFromCartForm, UserRegistrationForm, CustomAuthenticationForm
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
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .tokens import account_activation_token
from .forms import UserRegistrationForm, CustomAuthenticationForm, ContactForm
from .models import Product, Smartphone, Smartwatch, BlogPost,Testimonial, CartItem


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the latest three blog posts from the database
        latest_posts = BlogPost.objects.order_by('-date_published')[:3]
        context['latest_posts'] = latest_posts

        # Fetch the latest smartwatches from the database
        latest_smartwatches = Smartwatch.objects.order_by('-id')[:5]  
        context['latest_smartwatches'] = latest_smartwatches

        # Fetch the latest smartphones from the database
        latest_smartphones = Smartphone.objects.order_by('-id')[:5] 
        context['latest_smartphones'] = latest_smartphones

        testimonials = Testimonial.objects.all()[:2]  
        context['testimonials'] = testimonials

        return context
    
    
class BlogView(ListView):
    template_name = 'blog.html'  # Update with your actual template name
    context_object_name = 'latest_posts'
    model = BlogPost
    ordering = ['-date_published']  # Order posts by date_published, modify as needed
    paginate_by = 3

class ProductListView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'  

    def get_queryset(self):
        smartphones = Smartphone.objects.all()
        smartwatches = Smartwatch.objects.all()
        return {'smartphones': smartphones, 'smartwatches': smartwatches}


class AddToCartView(View):
    template_name = 'add_to_cart.html'

    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        print(f"Product ID: {product_id}")

        cart_items = self.request.session.get('cart_items', [])

        product_in_cart = next((item for item in cart_items if item['product_id'] == product_id), None)

        if product_in_cart:
            product_in_cart['quantity'] += 1
        else:
            cart_items.append({'product_id': product_id, 'quantity': 1})

        self.request.session['cart_items'] = cart_items

        # Pass the cart_items to the template
        return render(self.request, self.template_name, {'cart_items': cart_items})
    
    def get(self, request, *args, **kwargs):
        # Get the existing cart_items or an empty list
        cart_items = self.request.session.get('cart_items', [])
        # Pass the cart_items to the template
        return render(self.request, self.template_name, {'cart_items': cart_items})


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        # Your logic to remove item from the cart goes here
        # ...

        # Assuming you have successfully removed the item from the cart
        messages.success(request, 'Item removed from the cart.')
        
        # Redirect to the addtocart.html template
        return redirect('add_to_cart')  # Replace 'add_to_cart' with the actual URL name or path


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