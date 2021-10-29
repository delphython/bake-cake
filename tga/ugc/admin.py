from django.contrib import admin

from .forms import ProfileForm
from .models import Message
from .models import Profile
from .models import Levels
from .models import Forms
from .models import Topping
from .models import Berries
from .models import Decors


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "name",
    )
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "profile",
        "text",
        "created_at",
    )


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
