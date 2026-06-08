from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','username','email']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # Include all fields from the Room model
        exclude = ['host', 'participants']  # Exclude these fields

class UserForm(ModelForm):
    class Meta:
        model = User  # Corrected to reference the User model directly
        fields = ['username', 'email','avatar','bio']  # Specify the fields to include
