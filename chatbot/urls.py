

from django.urls import path


from . import views




app_name = 'chatbot'
urlpatterns = [
    path('', views.index, name='index'),
    path('genresp/', views.genresp, name='genresp'),
    path('cvmodule/',views.cvmodule, name='cvmodule'),

]