# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from products.views import all_products
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', view.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('reviews/', include('reviews.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'), 
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
