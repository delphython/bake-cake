from django.contrib import admin

from .models import Levels
from .models import Forms
from .models import Topping
from .models import Berries
from .models import Decors
from .models import OrderStatuses
from .models import Customers
from .models import Orders


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cost",
    )
    list_edit = (
        "name",
        "cost",
    )


@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cost",
    )
    list_edit = (
        "name",
        "cost",
    )


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cost",
    )
    list_edit = (
        "name",
        "cost",
    )


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cost",
    )
    list_edit = (
        "name",
        "cost",
    )


@admin.register(Decors)
class DecorsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cost",
    )
    list_edit = (
        "name",
        "cost",
    )


@admin.register(OrderStatuses)
class OrderStatusesAdmin(admin.ModelAdmin):
    list_display = ("status",)
    list_edit = ("status",)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "phone_number",
        "first_name",
        "last_name",
        "address",
    )
    list_edit = (
        "telegram_id",
        "phone_number",
        "first_name",
        "last_name",
        "address",
    )


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "title",
        "comment",
        "delivery_address",
        "delivery_date",
        "delivery_time",
        "cost",
        "status",
        "level",
        "form",
        "topping",
        "berries",
        "decor",
    )
    list_edit = (
        "title",
        "comment",
        "delivery_address",
        "delivery_date",
        "delivery_time",
        "cost",
        "decor",
    )
    list_filter = ("status",)
