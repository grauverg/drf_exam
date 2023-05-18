from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('status', views.StatusViewSet, basename='status')


urlpatterns = [
    path('', include(router.urls)),
    path('news/', views.NewsListCreateAPIView.as_view()),
    path('news/<int:pk>/', views.NewsRetrieveDestroyUpdateAPIView.as_view()),
    path('news/<int:news_id>/comment/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comment/<int:pk>/', views.CommentRetrieveDestroyUpdateAPIView.as_view()),
    path('news/<int:news_id>/<slug>/', views.NewsStatusCreateAPIView.as_view()),
    path('news/<int:news_id>/comment/<int:pk>/<slug>', views.CommentStatusCreateAPIView.as_view())
]
