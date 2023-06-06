from django.contrib import admin
from django.db.models import Count, Q, Value, Sum
from django.http.request import HttpRequest
from utility.pcloud import getPubSmallThumb, deleteFile
from . models import Stream, PortfolioImage, Plan, PlanAddon, ClientRequest
from django.utils.html import format_html

from core.views import getAuth


# ------------------------------- Customer Feedbacks--------------------------------------------------------------------------------------------
@admin.register(ClientRequest)
class FeedbackAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    icon_name = "chrome_reader_mode"
    name = "Client Appointments"
    list_display = ['bookedBy', 'reason', 'isVisible']


# -------------------------------Stream Admin--------------------------------------------------------------------------------------------
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    icon_name = "ondemand_video"
    list_display = ['title', 'streamLink', 'Thumbnail']
    search_fields = ['title']
    list_per_page = 10

    def Thumbnail(self, stream):
        component = f"""
            <a href="{stream.link}" target="_blank">
                <div style="width: 10rem;
                    height: 5.5rem;
                    background-image: url({getPubSmallThumb(stream.pubCode, 300)});
                    background-size: cover;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 0px 10px 0 #0000006e;
                    border-radius: 0.5rem;">
                </div>
	        </a>
        """
        return format_html(component)

    fieldsets = (
        (None, {
            "fields": (('title'), 'streamLink', 'thumbnail'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for object in queryset:
            response = deleteFile(
                getAuth(), object.pcloudFileId)
            if response == 200:
                continue
            else:
                break
        else:
            return super().delete_queryset(request, queryset)


# -------------------------------Portfolio Admin--------------------------------------------------------------------------------------------
@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    icon_name = "photo_library"
    list_display = ['category', 'Image',
                    'isHeroBackground', 'isHeroPic', 'isScrollPic', 'isEmotionalCapture', 'isPortfolioDisplay']
    list_filter = ['category']
    autocomplete_fields = ['category']
    list_per_page = 10
    list_display_links = None
    actions_selection_counter = False

    def Image(self, image):
        component = f"""
            <a href="{image.link}" target="_blank">
                <div style="width: 10rem;
                    height: 5.5rem;
                    background-image: url({getPubSmallThumb(image.pubCode, 300)});
                    background-size: cover;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 0px 10px 0 #0000006e;
                    border-radius: 0.5rem;">
                </div>
	        </a>
        """
        return format_html(component)

    fieldsets = (
        (None, {
            "fields": ('category', 'image', 'isHeroBackground', 'isHeroPic', 'isScrollPic', 'isEmotionalCapture', 'isPortfolioDisplay'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for object in queryset:
            response = deleteFile(
                getAuth(), object.pcloudFileId)
            if response == 200:
                continue
            else:
                break
        else:
            return super().delete_queryset(request, queryset)


# -------------------------------Plans--------------------------------------------------------------------------------------------
class AddonInline(admin.TabularInline):
    model = PlanAddon
    min_num = 1
    max_num = 100
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    icon_name = 'view_carousel'
    list_display = ['title', 'price', 'queries',]
    ordering = ['-price']

    inlines = [AddonInline]

    @admin.display(ordering='query_count')
    def queries(self, plan):
        return plan.query_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(query_count=Count('planquerie', distinct=True))

