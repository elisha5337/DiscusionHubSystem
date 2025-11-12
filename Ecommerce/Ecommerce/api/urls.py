from django .urls import path

from Ecommerce.api import views

urlpatterns=[
    path('',views.getRoutes),
    path('rooms/',views.getRooms),
    path('room/<str:pk>/',views.getRoom)
]