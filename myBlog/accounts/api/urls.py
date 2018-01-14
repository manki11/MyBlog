from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    # path('<int:pk>/', views.CommentDetailAPIView.as_view(), name='thread'),

]
