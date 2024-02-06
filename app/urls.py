from django.urls import path

from .views import (
    IndexView,
    ShopView,
    CartView,
    AddToCartView,
    RemoveFromCartView,CheckoutView,
    SignupView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,RedirectToIndexView,
    ActivateAccountView,ContactView,BlogView,ThankYouView,ContactSuccessView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
  #  path('<slug:category_slug>/', ShopView.as_view(), name='product-list-by-category'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('thankyou/', ThankYouView.as_view(), name='thankyou'),
    path('redirect-to-index/', RedirectToIndexView.as_view(), name='redirect-to-index'),
    
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/contact-success/', ContactSuccessView.as_view(), name='contact-success'),
    path('blog/', BlogView.as_view(), name='blog'), 

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', PasswordResetDoneView.as_view(), name='password-change-done'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
]
