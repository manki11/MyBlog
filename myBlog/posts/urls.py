from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    path('', views.post_list,),
    path('create/', views.post_create, name='create'),
    path('<slug:post_slug>/', views.post_details, name='detail'),
    path('<slug:post_slug>/edit/', views.post_update, name='update'),
    path('<slug:post_slug>/delete/', views.post_delete, name='delete')
]
