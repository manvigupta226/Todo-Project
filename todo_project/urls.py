from django.contrib import admin
from django.urls import path, include
from todo_app.views import signup_view, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view),
    path('login/', login_view),
    path('', include('todo_app.urls')),
]
