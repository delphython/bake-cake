from environs import Env
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from telegram.utils.request import Request


from ugc.models import (
    Message,
    Profile,
    Customers,
    OrderStatuses,
    Levels,
    Forms,
    Topping,
    Berries,
    Decors,
    Orders,
)

(
    FIRST,
    COMMENTS,
    DELIVERY_ADDRESS,
    DELIVERY_DATE,
    DELIVERY_TIME,
    ORDER_CAKE,
) = range(6)
(
    LEVELS,
    EXIT,
    COMPLITED_ORDERS,
    START_OVER,
    FORM,
    TOPPING,
    BERRIES,
    DECOR,
    TITLE,
    COMMENTS,
    SHOW_COST,
    INPUT_LEVELS,
) = range(12)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Произошла ошибка: {e}"
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            "name": update.message.from_user.username,
        },
    )
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

    reply_text = f"Ваш ID = {chat_id}\n{text}"
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    reply_keyboard = [["count"]]
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            "name": update.message.from_user.username,
        },
    )
    count = Message.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f"У вас {count} сообщений",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )


@log_errors
def start(update, context):
    global _telegram_id
    _telegram_id = "11225544"
    keyboard = [
        [
            InlineKeyboardButton("Собрать торт", callback_data=str(LEVELS)),
            InlineKeyboardButton(
                "Сделанные заказы", callback_data="COMPLITED_ORDERS"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return FIRST


@log_errors
def start_over(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton("Собрать торт", callback_data=str(LEVELS)),
            InlineKeyboardButton(
                "Сделанные заказы", callback_data=str(COMPLITED_ORDERS)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return FIRST


@log_errors
def levels(update, context):
    query = update.callback_query
    bot = context.bot

    levels = Levels.objects.all()
    keyboard = []

    for level in levels:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=level.name, callback_data=f"FORM|{level.name}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите Количество уровней",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def form(update, context):
    global _level
    query = update.callback_query
    _, _level = query.data.split("|")
    # query.edit_message_text(text="Вы выбрали: {_level}")
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали уровень: {_level}",
    )
    forms = Forms.objects.all()
    keyboard = []

    for form in forms:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=form.name, callback_data=f"TOPPING|{form.name}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите форму:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def topping(update, context):
    global _form
    query = update.callback_query
    _, _form = query.data.split("|")
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали форму: {_form}",
    )
    toppings = Topping.objects.all()
    keyboard = []

    for topping in toppings:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=topping.name, callback_data=f"BERRIES|{topping.name}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите топпинг:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def berries(update, context):
    global _topping
    query = update.callback_query
    _, _topping = query.data.split("|")
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали топпинг: {_topping}",
    )
    berries = Berries.objects.all()
    keyboard = []

    for berry in berries:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=berry.name, callback_data=f"DECOR|{berry.name}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите ягоды:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def decor(update, context):
    global _berries
    global _message_id
    global _chat_id
    query = update.callback_query
    _message_id = query.message.message_id
    _chat_id = query.message.chat_id
    _, _berries = query.data.split("|")
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали ягоды: {_berries}",
    )
    decors = Decors.objects.all()
    keyboard = []

    for decor in decors:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=decor.name, callback_data=f"TITLE|{decor.name}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите декор:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def title(update, context):
    global _decor
    query = update.callback_query
    _, _decor = query.data.split("|")
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали декор: {_decor}",
    )
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text="Мы можем разместить на торте любую надпись, например: «С днем рождения!»",
    )
    return COMMENTS


@log_errors
def comments(update, context):
    global _title_cost
    global _title
    global _message_id
    global _chat_id
    # query = update.callback_query
    bot = context.bot
    if update.message.text:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Вы выбрали надпись: {update.message.text}",
        )
        _title = update.message.text
        _title_cost = 500
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Введите комментарий к заказу:",
    )

    return DELIVERY_ADDRESS


@log_errors
def delivery_address(update, context):
    global _message_id
    global _chat_id
    global _telegram_id
    global _comment
    global _current_address

    customer = Customers.objects.get(telegram_id=_telegram_id)
    bot = context.bot
    if update.message.text:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Ваш комментарий к заказу: {update.message.text}",
        )
    _comment = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text="""Введите новый адрес доставки или нажмите
                Ввод, если желаете оставить текущий адрес:""",
    )
    bot.send_message(
        chat_id=update.message.chat_id,
        text=customer.address,
    )
    _current_address = customer.address

    return DELIVERY_DATE


@log_errors
def delivery_date(update, context):
    global _message_id
    global _chat_id
    global _current_address
    global _delivery_address
    # query = update.callback_query
    bot = context.bot
    if update.message.text:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Вы выбрали новый адрес: {update.message.text}",
        )
        _delivery_address = update.message.text
    else:
        _delivery_address = _current_address
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Введите дату доставки в формате дд.мм.гггг:",
    )

    return DELIVERY_TIME


@log_errors
def delivery_time(update, context):
    global _message_id
    global _chat_id
    # query = update.callback_query
    bot = context.bot
    if update.message.text:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Вы выбрали дату доставки: {update.message.text}",
        )
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Вебирите время доставки:",
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "с 08:00 по 12:00", callback_data="ORDER_CAKE|с 08:00 по 12:00"
            )
        ],
        [
            InlineKeyboardButton(
                "с 12:00 по 16:00", callback_data="ORDER_CAKE|с 12:00 по 16:00"
            )
        ],
        [
            InlineKeyboardButton(
                "с 16:00 по 20:00", callback_data="ORDER_CAKE|с 16:00 по 20:00"
            )
        ],
        [
            InlineKeyboardButton(
                "с 20:00 по 24:00", callback_data="ORDER_CAKE|с 20:00 по 24:00"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Вебирите время доставки:", reply_markup=reply_markup
    )
    return FIRST


@log_errors
def order_cake(update, context):
    global _delivery_time
    bot = context.bot
    query = update.callback_query
    _, _delivery_time = query.data.split("|")
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Вы выбрали время доставки: {_delivery_time}",
    )
    order_cost = save_order()

    keyboard = [
        [
            InlineKeyboardButton(
                "Заказать торт", callback_data=str(SHOW_COST)
            ),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text=f"Сумма заказа: {order_cost} руб.",
        reply_markup=reply_markup,
    )
    update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return FIRST


@log_errors
def save_order():
    global _level
    global _form
    global _topping
    global _berries
    global _decor
    global _delivery_time
    global _title
    global _comment
    global _delivery_address

    level = Levels.objects.get(name=_level)
    form = Forms.objects.get(name=_form)
    topping = Topping.objects.get(name=_topping)
    berries = Berries.objects.get(name=_berries)
    decor = Decors.objects.get(name=_decor)
    customer = Customers.objects.get(telegram_id="11225544")
    title = _title
    comment = _comment
    delivery_address = _delivery_address
    delivery_date = "2021-11-01"
    delivery_time = _delivery_time
    cost = level.cost + form.cost + topping.cost + berries.cost + decor.cost
    status = OrderStatuses.objects.get(status="готовим ваш торт")

    order = Orders(
        level=level,
        form=form,
        topping=topping,
        berries=berries,
        decor=decor,
        customer=customer,
        title=title,
        comment=comment,
        delivery_address=delivery_address,
        delivery_date=delivery_date,
        delivery_time=delivery_time,
        cost=cost,
        status=status,
    )
    order.save()

    return cost


@log_errors
def show_cost(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton(
                "Собрать еще торт", callback_data=str(LEVELS)
            ),
            InlineKeyboardButton("Выход", callback_data=str(EXIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def get_orders_text(t_id):
    orders_text = []
    orders = Orders.objects.filter(customer__telegram_id=t_id)
    for order in orders:
        orders_text.append(
            f"Заказ № {order.id}\n"
            + f"Стоимость торта: {order.cost} руб.\n"
            + f"Дата заказа: {order.delivery_date}\n"
            + f"Время заказа: {order.delivery_time}\n"
            + f"Статус заказа: {order.status.status}"
        )
    return orders_text


@log_errors
def complited_orders(update, context):
    orders_text = get_orders_text("11225544")
    query = update.callback_query
    bot = context.bot
    for order_text in orders_text:
        bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=order_text,
        )

    keyboard = [
        [
            InlineKeyboardButton("Собрать торт", callback_data=str(LEVELS)),
            InlineKeyboardButton("Выход", callback_data=str(EXIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def end(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text="Всего Вам хорошего!",
    )
    return ConversationHandler.END


class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        env = Env()
        env.read_env()
        TG_TOKEN = env.str("TG_TOKEN")

        # 1 -- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=TG_TOKEN,
            base_url=getattr(settings, "PROXY_URL", None),
        )
        # print(bot.get_me())

        # 2 -- обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                COMMENTS: [
                    MessageHandler(Filters.text & ~Filters.command, comments)
                ],
                DELIVERY_ADDRESS: [
                    MessageHandler(
                        Filters.text & ~Filters.command, delivery_address
                    )
                ],
                DELIVERY_DATE: [
                    MessageHandler(
                        Filters.text & ~Filters.command, delivery_date
                    )
                ],
                DELIVERY_TIME: [
                    MessageHandler(
                        Filters.text & ~Filters.command, delivery_time
                    )
                ],
                FIRST: [
                    CallbackQueryHandler(
                        levels, pattern="^" + str(LEVELS) + "$"
                    ),
                    CallbackQueryHandler(form, pattern="^FORM.*"),
                    CallbackQueryHandler(topping, pattern="^TOPPING.*"),
                    CallbackQueryHandler(berries, pattern="^BERRIES.*"),
                    CallbackQueryHandler(decor, pattern="^DECOR.*"),
                    CallbackQueryHandler(title, pattern="^TITLE.*"),
                    CallbackQueryHandler(
                        comments, pattern="^" + str(COMMENTS) + "$"
                    ),
                    CallbackQueryHandler(
                        delivery_address,
                        pattern="^" + str(DELIVERY_ADDRESS) + "$",
                    ),
                    CallbackQueryHandler(
                        delivery_date, pattern="^" + str(DELIVERY_DATE) + "$"
                    ),
                    CallbackQueryHandler(
                        delivery_time, pattern="^" + str(DELIVERY_TIME) + "$"
                    ),
                    CallbackQueryHandler(order_cake, pattern="^ORDER_CAKE.*"),
                    CallbackQueryHandler(
                        show_cost, pattern="^" + str(SHOW_COST) + "$"
                    ),
                    CallbackQueryHandler(
                        complited_orders,
                        pattern="^COMPLITED_ORDERS.*",
                    ),
                    CallbackQueryHandler(end, pattern="^" + str(EXIT) + "$"),
                    CallbackQueryHandler(
                        start_over, pattern="^" + str(START_OVER) + "$"
                    ),
                ],
            },
            fallbacks=[CommandHandler("start", start)],
        )

        updater.dispatcher.add_handler(conv_handler)

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
        updater.start_polling()
        updater.idle()
