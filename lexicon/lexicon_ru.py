LEXICON_RU: dict[str, str] = {
    'help_command': 'Это бот для отслеживания цен на товары с Ozon. Для его запуска напишите /start',
    'random_message': 'Это немного не так работает... Для работы с ботом напишите /start',
    'registration_start': 'Для начала работы с ботом нужно зарегистрироваться. Это нужно для персонализации результатов. '
                    '\nДля старта регистрации вызовите команду /registrate',
    'registration_error': 'Вы не зарегистрированы. \nДля старта регистрации вызовите команду /registrate',
    'registration_command': 'Приветствую в системе регистрации. Ответьте на несколько простых вопросов',
    'registration_card': 'У вас есть Ozon карта?',
    'registration_card_error': 'Ошибка. Ответьте на вопрос "да" или "нет"',
    'registration_variation': 'Какие вариации товара показывать?',
    'registration_variation_all': 'Все',
    'registration_variation_only_cheap': 'Только более дешёвые',
    'registration_variation_error': 'Ошибка. Ответьте на вопрос "все" или "только более дешёвые"',
    'registration_image': 'Показывать ли изображение товара на его страничке?',
    'registration_image_error': 'Ошибка. Ответьте на вопрос "да" или "нет"',
    'registration_notifications': 'Присылать ли вам уведомлении при изменении цены на товар из избранного?',
    'registration_notifications_only_lowering': 'Только при понижении цены',
    'registration_notifications_error': 'Ошибка. Ответьте на вопрос "да", "нет" или "только про понижения цены"',
    'registration_finish': 'Регистрация успешно завершена!',
    'registration_already_completed': 'Вы уже зарегистрированы',
    'main_menu_hello': 'Приветствую, {event.from_user.username}!',
    'main_menu_hello_2': 'Выберите действие',
    'main_menu_products': '👁️ Посмотреть цену на продукт',
    'main_menu_settings': '⚙️ Настройки',
    'main_menu_favorites': '⭐ Избранное',
    'main_menu_statistics': '📊 Статистика',
    'main_menu_add_admin': '➕ Добавить админа',
    'main_menu_about': 'ℹ️ О приложении',
    'about': 'Данный бот позволяет отслеживать цены на товары с Ozon. \nНаписан на aiogram в качестве курсовой работы \n\nАвтор: @csharpguy',
    'statistics_users': 'Количество пользователей: {users_count}',
    'statistics_products': 'Количество товаров: {products_count}',
    'statistics_brands': 'Количество продавцов: {sellers_count}',
    'add_admin': 'Пришлите имя аккаунта нового админа',
    'admin_added': 'Админ был успешно добавлен!',
    'admin_add_error': 'Пользователя с таким именем не существует. Попробуйте снова',
    'settings_all': 'Настройки пользователя {event.from_user.username}',
    'settings_have_card': 'Наличие Ozon карты',
    'have_card_description': 'В зависимости от того, есть ли у вас Ozon карта или нет, вам будут показываться соответствующие цены на товары',
    'have_card_checkbox': 'Ozon карта',
    'settings_show_variations': 'Отображение вариантов товара',
    'show_variations_description': 'Вместе с подробной информацией о товаре будет дополнительно выводиться список вариантов товара',
    'settings_show_image': 'Показывать изображение товара',
    'show_image_description': 'При включении настройки вместе с графиком изменения цены будет изображение товара',
    'show_image_checkbox': 'Показывать изображение товара',
    'settings_send_notifications': 'Уведомления',
    'send_notifications_description': 'При изменении цены на товар вам пришлют уведомление',
    'product_get_id': 'Отправьте мне ссылку на товар или его артикул. \nЛибо же просто напишите название товара и я постараюсь найти для вас возможные варианты',
    'favorites_show': 'Список ваших избранных товаров. Нажмите на товар для подробной информации',
    'favorites_edit': 'Нажмите на товар чтобы удалить его из избранного',
    'UserShowVariations.all': 'Все',
    'UserShowVariations.only_cheaper': 'Только более дешёвые',
    'UserSendNotifications.yes': 'Присылать',
    'UserSendNotifications.no': 'Не присылать',
    'UserSendNotifications.only_lowering': 'Присылать только при понижении цены',
    'product_search': 'По запросу "{dialog_data[search_query]}" были найдены следующие результаты',
    'product_search_error': 'По запросу "{dialog_data[search_query]}" не было найдено никаких результатов',
    'product_id_error': 'Товара с таким артикулом не существует',
    'product_price_have_card': 'Цена на данный момент: {dialog_data[product][card_price]} руб.',
    'product_price_no_card': 'Цена на данный момент: {dialog_data[product][regular_price]} руб.',
    'product_variant_have_card': '{item[card_price]} руб. — {item[title]}',
    'product_variant_no_card': '{item[regular_price]} руб. — {item[title]}',
    'product_rating_count': '★ {dialog_data[product][rating]} • {dialog_data[product][rating_count]}  отзывов',
    'product_no_variations': 'Вариантов нет',
    'product_show_variations': '🔢 Показать варианты',
    'product_hide_variations': '↪️ Скрыть варианты',
    'product_to_favorites': '⭐ В избранное',
    'product_from_favorites': '⭐ Удалить из избранного',
    'favorites_edit_button': '✏️ Редактировать',
    'favorites_empty': 'У вас нет товаров в избранном',
    'cancel': '❌ Отмена',
    'close': '❌ Закрыть',
    'back': '⬅️ Назад',
    'yes': 'Да',
    'no': 'Нет',
}
