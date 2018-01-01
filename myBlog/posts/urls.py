from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list),
    path('create/', views.post_create),
    path('<int:post_id>/', views.post_details),
    path('<int:post_id>/update', views.post_update),
    path('<int:post_id>/delete', views.post_delete)
]
