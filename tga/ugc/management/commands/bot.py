from environs import Env
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
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

FIRST, SECOND = range(2)
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
    DELIVERY_ADDRESS,
    DELIVERY_DATE,
    DELIVERY_TIME,
    ORDER_CAKE,
    SHOW_COST,
    INPUT_LEVELS,
) = range(16)


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
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def levels(update, context):
    query = update.callback_query
    bot = context.bot

    levels = Levels.objects.all()
    keyboard = []

    for level in levels:
        keyboard.append(
            InlineKeyboardButton(text=level.name, callback_data="FORM")
        )

    new_keyboard = [keyboard]
    new_keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(new_keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Количество уровней",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def form(update, context):
    query = update.callback_query
    bot = context.bot
    forms = Forms.objects.all()
    keyboard = []

    for form in forms:
        keyboard.append(
            InlineKeyboardButton(text=form.name, callback_data="TOPPING")
        )

    new_keyboard = [keyboard]
    new_keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    print()
    reply_markup = InlineKeyboardMarkup(new_keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def topping(update, context):
    query = update.callback_query
    bot = context.bot
    toppings = Topping.objects.all()
    keyboard = []

    for topping in toppings:
        keyboard.append(
            InlineKeyboardButton(text=topping.name, callback_data="BERRIES")
        )

    new_keyboard = [keyboard]
    new_keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(new_keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def berries(update, context):
    query = update.callback_query
    bot = context.bot
    berries = Berries.objects.all()
    keyboard = []

    for berry in berries:
        keyboard.append(
            InlineKeyboardButton(text=berry.name, callback_data="DECOR")
        )

    new_keyboard = [keyboard]
    new_keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(new_keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def decor(update, context):
    query = update.callback_query
    bot = context.bot
    decors = Decors.objects.all()
    keyboard = []

    for decor in decors:
        keyboard.append(
            InlineKeyboardButton(text=decor.name, callback_data="TITLE")
        )

    new_keyboard = [keyboard]
    new_keyboard.append(
        [
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(new_keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def title(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton("Надпись", callback_data=str(COMMENTS)),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def comments(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton(
                "Комментарий к заказу", callback_data=str(DELIVERY_ADDRESS)
            ),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def delivery_address(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton(
                "Адрес доставки", callback_data=str(DELIVERY_DATE)
            ),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def delivery_date(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton(
                "Дата доставки", callback_data=str(DELIVERY_TIME)
            ),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def delivery_time(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton(
                "Время доставки", callback_data=str(ORDER_CAKE)
            ),
            InlineKeyboardButton(
                "Отменить выполнение заказа", callback_data=str(START_OVER)
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def order_cake(update, context):
    query = update.callback_query
    bot = context.bot
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
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Выберите действие:",
        reply_markup=reply_markup,
    )
    return FIRST


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
        text="Сумма заказа:",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def complited_orders(update, context):
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [
            InlineKeyboardButton("Собрать торт", callback_data=str(LEVELS)),
            InlineKeyboardButton("Выход", callback_data=str(EXIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Ваши заказы",
        reply_markup=reply_markup,
    )
    return FIRST


@log_errors
def end(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
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
                FIRST: [
                    CallbackQueryHandler(
                        levels, pattern="^" + str(LEVELS) + "$"
                    ),
                    # CallbackQueryHandler(form, pattern="^" + str(FORM) + "$"),
                    CallbackQueryHandler(form, pattern="^FORM$"),
                    CallbackQueryHandler(topping, pattern="^TOPPING$"),
                    CallbackQueryHandler(berries, pattern="^BERRIES$"),
                    CallbackQueryHandler(decor, pattern="^DECOR$"),
                    CallbackQueryHandler(title, pattern="^TITLE$"),
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
                    CallbackQueryHandler(
                        order_cake, pattern="^" + str(ORDER_CAKE) + "$"
                    ),
                    CallbackQueryHandler(
                        show_cost, pattern="^" + str(SHOW_COST) + "$"
                    ),
                    CallbackQueryHandler(
                        complited_orders,
                        pattern="^" + str(COMPLITED_ORDERS) + "$",
                    ),
                    CallbackQueryHandler(end, pattern="^" + str(EXIT) + "$"),
                    CallbackQueryHandler(
                        start_over, pattern="^" + str(START_OVER) + "$"
                    ),
                ],
            },
            fallbacks=[CommandHandler("start", start)],
        )

        # message_handler = MessageHandler(Filters.text, do_echo)
        # updater.dispatcher.add_handler(message_handler)
        # updater.dispatcher.add_handler(CommandHandler("count", do_count))
        # updater.dispatcher.add_handler(CommandHandler("starting", do_starting))
        updater.dispatcher.add_handler(conv_handler)

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
