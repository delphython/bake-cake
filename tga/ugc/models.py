from django.db import models


class Profile(models.Model):  # from template
    external_id = models.PositiveIntegerField(
        verbose_name="Внешний ID пользователя",
        unique=True,
    )
    name = models.TextField(
        verbose_name="Имя пользователя",
    )

    def __str__(self):
        return f"#{self.external_id} {self.name}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Message(models.Model):  # from template
    profile = models.ForeignKey(
        to="ugc.Profile",
        verbose_name="Профиль",
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    created_at = models.DateTimeField(
        verbose_name="Время получения",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Сообщение {self.pk} от {self.profile}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


# Add models here
class Customers(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в телеграмме",
        unique=True,
    )
    phone_number = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Номер телефона заказчика",
    )
    first_name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Имя заказчика",
    )
    last_name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Фамилия заказчика",
    )
    address = models.TextField(
        verbose_name="Адрес заказчика",
    )

    def __str__(self):
        return f"Заказчик {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class OrderStatuses(models.Model):
    status = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Номер телефона заказчика",
    )

    def __str__(self):
        return "Статусы заказов"

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"


class Levels(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Наимнование уровня",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена уровня",
    )

    def __str__(self):
        return "Количество уровней"

    class Meta:
        verbose_name = "Количество уровней"
        verbose_name_plural = "Количество уровней"


class Forms(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Наимнование формы",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена формы",
    )

    def __str__(self):
        return "Формы"

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"


class Topping(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Наимнование топпинга",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена топпинга",
    )

    def __str__(self):
        return "Топпинг"

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинг"


class Berries(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Название ягоды",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена ягоды",
    )

    def __str__(self):
        return "Ягода"

    class Meta:
        verbose_name = "Ягода"
        verbose_name_plural = "Ягоды"


class Decors(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Наименование декора",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена декора",
    )

    def __str__(self):
        return "Декор"

    class Meta:
        verbose_name = "Декор"
        verbose_name_plural = "Декор"


class Orders(models.Model):
    customer = models.ForeignKey(
        to="ugc.Customers",
        verbose_name="Заказчик",
        on_delete=models.PROTECT,
    )
    title = models.TextField(
        verbose_name="Надпись",
    )
    comment = models.TextField(
        verbose_name="Комментарий к заказу",
    )
    delivery_address = models.TextField(
        verbose_name="Адрес доставки",
    )
    delivery_date = models.DateField(
        verbose_name="Дата доставки",
    )
    delivery_time = models.TimeField(
        verbose_name="Время доставки",
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость заказа",
    )
    status = models.ForeignKey(
        to="ugc.OrderStatuses",
        verbose_name="Статус заказа",
        null=True,
        on_delete=models.SET_NULL,
    )
    level = models.ForeignKey(
        to="ugc.Levels",
        verbose_name="Количество уровней",
        null=True,
        on_delete=models.SET_NULL,
    )
    form = models.ForeignKey(
        to="ugc.Forms",
        verbose_name="Форма",
        null=True,
        on_delete=models.SET_NULL,
    )
    topping = models.ForeignKey(
        to="ugc.Topping",
        verbose_name="Топпинг",
        null=True,
        on_delete=models.SET_NULL,
    )
    berries = models.ForeignKey(
        to="ugc.Berries",
        verbose_name="Ягоды",
        null=True,
        on_delete=models.SET_NULL,
    )
    decor = models.ForeignKey(
        to="ugc.Decors",
        verbose_name="Декор",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"Заказ № {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
