from django.urls import path


from . import views


app_name = "app_accounts"


urlpatterns = [
    path("register_form/", views.sign_up_user, name="register_form"),
    path("login/", views.login_user, name="login"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("edit_profile/<str:username>/", views.edit_profile, name="edit_profile"),
    path("parking-history/", views.parking_history, name="parking_history"),
    path("parking/", views.parking_view, name="parking"),
    path("top_up_balance/", views.top_up_balance, name="top_up_balance"),
    path("pay_parking/<int:record_id>/", views.pay_parking, name="pay_parking"),
]
