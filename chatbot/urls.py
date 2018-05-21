

from django.urls import path


from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'chatbot'
urlpatterns = [
    path('', views.index, name='index'),
    path('genresp/', views.genresp, name='genresp'),
    path('cvmodule/',views.cvmodule, name='cvmodule'),
    path('application/',views.application, name='application'),
    path('mainpage/',views.mainpage, name='mainpage'),
    path('ratingpage/',views.ratingpage, name='ratingpage'),
    path('resultpage/',views.resultpage, name='resultpage'),
    path('usercheck/',views.usercheck, name='usercheck'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)