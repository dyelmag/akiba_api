from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('new/',   views.NewUserView.as_view(), name='new-user'),
    path('login/',   views.LoginView.as_view(), name='login'),
    #path('logout/',   views.Logout.as_view(), name='login'),
    path('perfil/',   views.PerfilView.as_view(), name='user-perfil'),

]
