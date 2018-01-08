from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    # path('create/', views.post_create, name='create'),
    path('<int:id>/', views.comment_thread, name='thread'),
    # path('<slug:post_slug>/edit/', views.post_update, name='update'),
    # path('<slug:post_slug>/delete/', views.post_delete, name='delete')
]