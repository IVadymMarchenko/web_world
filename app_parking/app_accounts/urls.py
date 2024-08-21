from django.urls import path


from . import views


app_name = "app_accounts"


urlpatterns = [
    path("register_form/", views.sign_up_user, name="register_form"),
    path("login/", views.login_user, name="login"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('parking-history/', views.ParkingHistoryView.as_view(), name='parking_history'),
    path('pay-parking/<int:pk>/', views.pay_parking, name='pay_parking'),

]
