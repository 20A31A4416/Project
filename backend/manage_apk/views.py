from rest_framework import viewsets
from .models import PortfolioImage, Plan, ClientRequest, Stream
from .serializers import PortfolioImageSerializer, PlanSerializer, ClientAppointmentSerializer, StreamSerializer


class PortfolioImageViewSet(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all().select_related(
        'category').order_by('-id')
    serializer_class = PortfolioImageSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class ClientAppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = ClientAppointmentSerializer

    def get_queryset(self):
        return ClientRequest.objects.filter(isVisible=True)


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all().order_by('-id')
    serializer_class = StreamSerializer
