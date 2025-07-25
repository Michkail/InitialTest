"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v2/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v2/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v2/investments/', include("apps.investments.urls")),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
