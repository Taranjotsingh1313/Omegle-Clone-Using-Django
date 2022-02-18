from unicodedata import name
from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name="index"),
    path("register/",views.register,name="register"),
    path("creatematch/",views.createMatch,name="createMatch"),
    path("video/<str:groupname>/<str:created>",views.videoChat,name="video"),
    path("login/",views.Login,name="login"),
    path("signup/",views.SignUp,name="signup"),
    path("logout/",views.Logout,name="logout"),
    path("skip/<str:groupname>/",views.Skip,name="skip"),
]