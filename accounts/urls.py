from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Existing login view
    path('register/', views.register, name='register'),  # Existing register view
    path('logout/', views.logout_view, name='logout'),  # Add this line for logout
]
