from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path("<str:username>/", views.profile_view, name="profile"),
    path("<str:username>/", views.profile_view, name="profile"),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("password-reset/confirm/", views.password_reset_confirm, name="password_reset_confirm"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete")

    
]
