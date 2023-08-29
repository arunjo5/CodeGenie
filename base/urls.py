from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('snippet/<str:pk>', views.snippet, name='snippet'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('create-snippet/', views.createSnippet, name='create-snippet'),
    path('auto-code/', views.autoCode, name='auto-code'),
    path('code-explain/', views.codeExplain, name='code-explain'),
    path('code-translate/', views.codeTranslate, name='code-translate')

]
