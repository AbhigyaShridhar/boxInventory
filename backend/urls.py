from django.urls import path
from . import views
from rest_framework.authtoken import views as tokenViews

app_name = "backend"

urlpatterns = [
    path('', views.index, name="index"),
    path('users/login', tokenViews.obtain_auth_token),
    path('users/register', views.Register.as_view(), name="register"),
    path('users/account', views.UserDetails.as_view(), name="user_details"),
    path('inventory/add', views.CreateBox.as_view(), name="create_box"),
    path('inventory/update/<int:pk>', views.UpdateBox.as_view(), name="update_box"),
    path('inventory/delete/<int:pk>', views.DeleteBox.as_view(), name="delete_box"),
    path('inventory/view', views.ListBoxes.as_view(), name="list_boxes"),
    path('users/inventory', views.ListUserBoxes.as_view(), name="user_boxes"),
]