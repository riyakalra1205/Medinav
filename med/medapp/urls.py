from django.urls import path
from . import views

urlpatterns = [path('', views.index, name='index'),
               path('search/',views.medinav,name='search'),
                path('consultation/',views.consultation,name='consultation_page'),
                 path('get_ai_response/', views.ai_response_view, name='get_ai_response'), # Root URL maps to the index view
]