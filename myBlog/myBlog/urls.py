"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import (login_view, register_view, logout_view)
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comments/', include('comments.urls', namespace='comments')),
    # Auth
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('', include('posts.urls', namespace='posts')),
    path('api/posts/', include('posts.api.urls', namespace='posts-api')),
    path('api/comments/', include('comments.api.urls', namespace='comments-api')),
    path('api/users/', include('accounts.api.urls', namespace='accounts-api')),
    path(r'^api-token-auth/', views.obtain_auth_token)

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
