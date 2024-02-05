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
    PasswordResetCompleteView,
    ActivateAccountView,ContactView,BlogView,ThankYouView,ContactSuccessView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
  #  path('<slug:category_slug>/', ShopView.as_view(), name='product_list_by_category'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('thankyou/', ThankYouView.as_view(), name='thankyou'),


    
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/contact_success/', ContactSuccessView.as_view(), name='contact_success'),
    path('blog/', BlogView.as_view(), name='blog'), 

    
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordResetDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
]

