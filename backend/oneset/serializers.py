from rest_framework import serializers
from .models import Category
from utility.pcloud import getPubSmallThumb


class CategorySerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField('getLink')

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
            'link'
        )

    def getLink(self, category: Category):
        return getPubSmallThumb(category.pubCode, 400, 1)
