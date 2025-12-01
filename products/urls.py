try:
    from django.urls import path  # type: ignore[import]
except Exception:
    # Fallback stub for environments without Django (avoids "could not be resolved" in editors)
    def path(route, view, name=None):
        return (route, view, name)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    # path('product/<int:pk>', views.product, name='product'),  
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
