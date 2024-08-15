from django.urls import path, include
from api import views
from .yasg import urlpatterns as url_doc

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('news', views.NewsViewSet)
router.register('gallery', views.PhotoViewSet)
router.register('photo-categories', views.PhotoCategoryViewSet)
router.register('events', views.EventViewSet)
router.register('halls', views.HallViewSet)
router.register('repertoires', views.RepertoireViewSet)
router.register('repertoire-seances', views.PerformanceSeanceViewSet)
router.register('carts', views.CartViewSet)
router.register('cart-tickets', views.CartTicketViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]

urlpatterns += url_doc