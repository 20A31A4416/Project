from django.urls import path, include
from rest_framework.routers import DefaultRouter

from manage_apk import views as manageApkView
from oneset import views as oneSetView

manageApkRouter = DefaultRouter()
manageApkRouter.register('portfolio', manageApkView.PortfolioImageViewSet)
manageApkRouter.register('plans', manageApkView.PlanViewSet)
manageApkRouter.register(
    'bookings', manageApkView.ClientAppointmentViewSet, basename='bookings')
manageApkRouter.register(
    'streams', manageApkView.StreamViewSet, basename='streams')

oneSetRouter = DefaultRouter()
manageApkRouter.register('categories', oneSetView.CategoryViewSet)

urlpatterns = [
    path('', include(manageApkRouter.urls)),
    path('', include(oneSetRouter.urls)),
]
