try:
    from django.urls import path  # type: ignore[import]
except Exception:
    # Fallback stub for environments without Django (avoids "could not be resolved" in editors)
    def path(route, view, name=None):
        return (route, view, name)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # temporary view — we will build page later
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]

    


