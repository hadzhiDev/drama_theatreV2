from django.contrib import admin
from django.utils.safestring import mark_safe

from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from core.models import *


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'get_image')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('date', )

    @admin.display(description='Обложка')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')


@admin.register(Photo)
class PhotoCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_image')
    list_display_links = ('id', 'created_at')
    search_fields = ('id', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='фотография')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')


@admin.register(PhotoCategory)
class PhotoCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'get_image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='фотография')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    list_display_links = ('id', 'full_name')
    search_fields = ('id', 'full_name')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    list_display_links = ('id', 'full_name')
    search_fields = ('id', 'full_name')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'repertoire_name', 'type', 'row_number', 'seat_number', 'is_sold')
    list_display_links = ('id', 'repertoire_name')
    search_fields = ('repertoire_name', 'row_number')
    readonly_fields = ('repertoire_name', 'row_number', 'seat_number', 'type')


class TicketTypeStackedInline(NestedTabularInline):
    model = TicketType
    extra = 1


class PerformanceSeanceStackedInline(NestedTabularInline):
    model = PerformanceSeance
    extra = 1
    inlines = [TicketTypeStackedInline, ]


# class PerformanceDayStackedInline(NestedTabularInline):
#     model = PerformanceDay
#     extra = 1
#     inlines = [PerformanceSeanceStackedInline,]
#     readonly_fields = ('created_at', 'updated_at',)


@admin.register(Repertoire)
class RepertoireAdmin(NestedModelAdmin):
    list_display = ('id', 'name', 'duration', 'pg', 'get_image')
    list_display_links = ('id', 'name', 'duration')
    search_fields = ('id', 'name', 'created_at')
    readonly_fields = ('created_at', 'updated_at', )
    inlines = [PerformanceSeanceStackedInline,]

    @admin.display(description='фотография')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')


class EmptySpaceStackedInline(NestedTabularInline):
    model = EmptySpace
    extra = 2


class HallRowStackedInline(NestedTabularInline):
    model = HallRow
    extra = 1
    inlines = [EmptySpaceStackedInline, ]


@admin.register(Hall)
class HallAdmin(NestedModelAdmin):
    list_display = ('id', 'name', 'created_at', 'get_image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [HallRowStackedInline, ]

    @admin.display(description='фотография')
    def get_image(self, item):
        return mark_safe(f'<img src="{item.image.url}" width="100px">')
