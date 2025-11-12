from django.contrib import admin
from django.urls import path
from .views import rooms, django_page, home, create_room, update_room, delete_room, loginPage, logoutUser, registerPage, \
    delete_message, profile, update_user, topicsPage, activityPage
from .views import Post  # Ensure you import the correct view function


urlpatterns = [
    path('', home, name="home"),
    path('logout/',logoutUser,name="logout"),
    path('register/',registerPage,name="register"),
    path('login/',loginPage,name="login"),
     path('rooms/<str:pk>',rooms,name="room"),
    path('django/',django_page,name="Django"),
    path('admin/', admin.site.urls),
    path('createroom/',create_room, name="create_room"),
    path('update_room/<str:pk>',update_room,name="update_room"),
    path('delete_room/<str:pk>',delete_room,name="delete_room"),
    path('delete_message/<str:pk>',delete_message,name="delete_message"),
    path('profile/<str:pk>',profile,name="profile"),
    path('update_user/',update_user,name="update_user"),
    path('topics/',  topicsPage, name="topics"),
    path('activity/',activityPage,name='activity')

]
