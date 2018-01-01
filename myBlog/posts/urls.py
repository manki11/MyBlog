from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    path('', views.post_list),
    path('create/', views.post_create, name='create'),
    path('<int:post_id>/', views.post_details, name='detail'),
    path('<int:post_id>/update', views.post_update, name='update'),
    path('<int:post_id>/delete', views.post_delete, name='delete')
]
