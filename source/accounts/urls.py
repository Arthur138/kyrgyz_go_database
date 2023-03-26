from django.urls import path
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import UserDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]
