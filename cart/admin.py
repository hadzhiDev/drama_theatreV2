from django.contrib import admin

from .models import TicketForSale, Cart


class TicketForSaleStackedInline(admin.StackedInline):
    model = TicketForSale
    extra = 1
    readonly_fields = ('price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'total_price',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'email', 'phone', 'address', )
    readonly_fields = ('total_price', )
    inlines = (TicketForSaleStackedInline,)
