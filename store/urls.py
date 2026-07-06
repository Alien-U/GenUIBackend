from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
<<<<<<< HEAD
  path("health/", views.health_check, name="health"),
=======
>>>>>>> d0cf1bbed744ff15a6acbf9b3951a34a8d813324
  path('register/', views.register_view),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
  # Post (Your new component)
  path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
  path('posts/', views.get_posts, name='post-list'),
  path('posts/<int:pk>/', views.get_post),
  path('lists/', views.get_lists),
  path('lists/add/', views.add_to_lists),
  path('lists/remove/', views.remove_from_lists),
  path('lists/update/', views.update_lists_quantity),
  # path('api/nvidia-proxy/', views.nvidia_proxy, name='nvidia_proxy'),
  # Fixed
# Adding <path:rest> allows the "chat/completions" part to be captured
  path('nvidia-proxy/<path:rest>', views.nvidia_proxy, name='nvidia_proxy'),
  # ------------------------------------
]