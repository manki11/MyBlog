from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='list'),
    # path('create/', views.post_create, name='create'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='detail'),
    # path('<slug:post_slug>/edit/', views.post_update, name='update'),
    # path('<slug:post_slug>/delete/', views.post_delete, name='delete')
]