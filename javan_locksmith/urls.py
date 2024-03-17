"""javan_locksmith URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from installation.views import search_request_view

urlpatterns = [
                  path('saheb-javan-kelid/', admin.site.urls),
                  # path("request/<str:web_id>", GetRequestView.as_view(), name="get-request-detail"),
                  path('', search_request_view, name="search-request")
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'installation.views.custom_404'
