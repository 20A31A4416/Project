from .models import Plan, PlanAddon
from rest_framework import serializers
from .models import PortfolioImage, Plan, PlanAddon, ClientRequest, Stream


class PortfolioImageSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = PortfolioImage
        fields = (
            'id',
            'category',
            'link',
            'isHeroBackground',
            'isHeroPic',
            'isScrollPic',
            'isPortfolioDisplay',
            'isEmotionalCapture',
        )


# ---------------------- Plans --------------------------------------------------------


class PlanAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanAddon
        fields = ('title',)


class PlanSerializer(serializers.ModelSerializer):
    addons = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ('title', 'price', 'addons')

    def get_addons(self, obj):
        addons = obj.addons.all()
        return [addon.title for addon in addons]

    def prefetch_related(self, queryset):
        queryset = super().prefetch_related(queryset)
        return queryset.prefetch_related('addons')

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.prefetch_related(queryset)


# ---------------------- Feedback --------------------------------------------------------
class ClientAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = '__all__'


# ---------------------- Streams --------------------------------------------------------
class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = ('id', 'title', 'streamLink', 'link', 'time')
