from django.urls import path
from . import views

app_name='comments'
urlpatterns = [
    path('create/', views.CommentCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', views.CommentDetailAPIView.as_view(), name='thread'),

]