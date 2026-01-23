# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from products.views import all_products

urlpatterns = [
    # path('', view.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
