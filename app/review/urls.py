from django.urls import path
from . import views

#   path('api/reviews/', include('review.urls')),

urlpatterns = [
    path('', views.ReviewListCreate.as_view()),
    path('<int:pk>/', views.ReviewRetrieveUpdateDestroy.as_view()),

]




