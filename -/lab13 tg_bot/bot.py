import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)
from main import Database

load_dotenv()
(
    NAME, 
    ORDER_ITEM, 
    DELIVERY_TIME,
    EDIT_CHOICE,
    EDIT_NAME,
    EDIT_ITEM,
    EDIT_TIME,
    DELETE_ORDER
) = range(8)
db = Database()

class OrderBot:
    def __init__(self):
        self.token = os.getenv('TOKEN')
        print(self.token)
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        
        self.application.add_handler(CommandHandler("start", self.start))
        
        self.application.add_handler(CommandHandler("basket", self.basket))
        
        
        order_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.start_order, pattern='^add_order$')],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_name)],
                ORDER_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_order_item)],
                DELIVERY_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_delivery_time)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        self.application.add_handler(order_conv_handler)
        
        
        edit_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.start_edit, pattern='^edit_order_')],
            states={
                EDIT_CHOICE: [CallbackQueryHandler(self.edit_choice_handler)],
                EDIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edit_name)],
                EDIT_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edit_item)],
                EDIT_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edit_time)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        self.application.add_handler(edit_conv_handler)
        
        delete_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.start_delete, pattern='^delete_order$')],
            states={
                DELETE_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.confirm_delete)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        self.application.add_handler(delete_conv_handler)
        self.application.add_handler(CallbackQueryHandler(self.view_orders, pattern='^view_orders$'))
        self.application.add_handler(CallbackQueryHandler(self.main_menu, pattern='^main_menu$'))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        await update.message.reply_text(
            "👋 Добро пожаловать в Order Manager Bot!\n\n"
            "Используйте команду /basket для управления заказами."
        )
    
    async def basket(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /basket - главное меню"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Добавить заказ", callback_data='add_order'),
                InlineKeyboardButton("📋 Посмотреть заказы", callback_data='view_orders'),
            ],
            [
                InlineKeyboardButton("✏️ Изменить заказ", callback_data='edit_menu'),
                InlineKeyboardButton("🗑️ Удалить заказ", callback_data='delete_order'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(
                "🛒 **Корзина заказов**\n\n"
                "Выберите действие:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.callback_query.edit_message_text(
                "🛒 **Корзина заказов**\n\n"
                "Выберите действие:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def start_order(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало создания заказа"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "📝 **Создание нового заказа**\n\n"
            "Шаг 1/3:\n"
            "Как вас зовут?"
        )
        return NAME
    
    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получение имени клиента"""
        context.user_data['customer_name'] = update.message.text
        await update.message.reply_text(
            "✅ Имя сохранено!\n\n"
            "Шаг 2/3:\n"
            "Что вы хотите заказать?"
        )
        return ORDER_ITEM
    
    async def get_order_item(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получение заказа"""
        context.user_data['order_item'] = update.message.text
        await update.message.reply_text(
            "✅ Заказ сохранен!\n\n"
            "Шаг 3/3:\n"
            "К какому времени вам привезти заказ?\n"
            "(Например: '15:30', 'к 18:00', 'через 2 часа')"
        )
        return DELIVERY_TIME
    
    async def get_delivery_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получение времени доставки и сохранение заказа"""
        delivery_time = update.message.text
        
        order_id = db.add_order(
            context.user_data['customer_name'],
            context.user_data['order_item'],
            delivery_time
        )
        
        await update.message.reply_text(
            f"🎉 **Заказ #{order_id} успешно создан!**\n\n"
            f"👤 Имя: {context.user_data['customer_name']}\n"
            f"📦 Заказ: {context.user_data['order_item']}\n"
            f"⏰ Время доставки: {delivery_time}\n\n"
            "Что хотите сделать дальше?",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
            ]])
        )
        
        context.user_data.clear()
        return ConversationHandler.END
    
    async def view_orders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Просмотр всех заказов"""
        query = update.callback_query
        await query.answer()
        
        orders = db.get_all_orders()
        
        if not orders:
            await query.edit_message_text(
                "📭 Заказов пока нет!\n\n"
                "Хотите создать первый заказ?",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("➕ Создать заказ", callback_data='add_order'),
                    InlineKeyboardButton("🔙 Назад", callback_data='main_menu')
                ]])
            )
            return
        
        message = "📋 **Список всех заказов:**\n\n"
        for order in orders:
            order_id, name, item, time, created_at = order
            message += (
                f"🔹 **Заказ #{order_id}**\n"
                f"👤 Клиент: {name}\n"
                f"📦 Заказ: {item}\n"
                f"⏰ Доставка: {time}\n"
                f"📅 Создан: {created_at}\n"
                f"{'-'*30}\n"
            )
        
        keyboard = []
        for order in orders[:10]:
            order_id = order[0]
            keyboard.append([
                InlineKeyboardButton(f"✏️ Заказ #{order_id}", callback_data=f'edit_order_{order_id}')
            ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Назад", callback_data='main_menu'),
            InlineKeyboardButton("➕ Новый заказ", callback_data='add_order')
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def start_edit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало редактирования заказа"""
        query = update.callback_query
        await query.answer()
        
        order_id = int(query.data.split('_')[2])
        context.user_data['edit_order_id'] = order_id
        
        order = db.get_order(order_id)
        
        if not order:
            await query.edit_message_text("Заказ не найден!")
            return ConversationHandler.END
        
        keyboard = [
            [InlineKeyboardButton("👤 Изменить имя", callback_data='edit_name')],
            [InlineKeyboardButton("📦 Изменить заказ", callback_data='edit_item')],
            [InlineKeyboardButton("⏰ Изменить время", callback_data='edit_time')],
            [InlineKeyboardButton("🔙 Назад", callback_data='view_orders')]
        ]
        
        await query.edit_message_text(
            f"✏️ **Редактирование заказа #{order_id}**\n\n"
            f"Текущие данные:\n"
            f"👤 Имя: {order[1]}\n"
            f"📦 Заказ: {order[2]}\n"
            f"⏰ Время: {order[3]}\n\n"
            "Что вы хотите изменить?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return EDIT_CHOICE
    
    async def edit_choice_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка выбора поля для редактирования"""
        query = update.callback_query
        await query.answer()
        
        choice = query.data
        
        if choice == 'edit_name':
            await query.edit_message_text("Введите новое имя:")
            return EDIT_NAME
        elif choice == 'edit_item':
            await query.edit_message_text("Введите новый заказ:")
            return EDIT_ITEM
        elif choice == 'edit_time':
            await query.edit_message_text("Введите новое время доставки:")
            return EDIT_TIME
    
    async def edit_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Редактирование имени"""
        new_name = update.message.text
        order_id = context.user_data['edit_order_id']
        
        db.update_order(order_id, customer_name=new_name)
        
        await update.message.reply_text(
            f"✅ Имя в заказе #{order_id} успешно изменено!\n\n"
            f"Новое имя: {new_name}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
            ]])
        )
        return ConversationHandler.END
    
    async def edit_item(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Редактирование заказа"""
        new_item = update.message.text
        order_id = context.user_data['edit_order_id']
        
        db.update_order(order_id, order_item=new_item)
        
        await update.message.reply_text(
            f"✅ Заказ #{order_id} успешно изменен!\n\n"
            f"Новый заказ: {new_item}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
            ]])
        )
        return ConversationHandler.END
    
    async def edit_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Редактирование времени доставки"""
        new_time = update.message.text
        order_id = context.user_data['edit_order_id']
        
        db.update_order(order_id, delivery_time=new_time)
        
        await update.message.reply_text(
            f"✅ Время доставки в заказе #{order_id} успешно изменено!\n\n"
            f"Новое время: {new_time}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
            ]])
        )
        return ConversationHandler.END
    
    async def start_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало процесса удаления"""
        query = update.callback_query
        await query.answer()
        
        
        orders = db.get_all_orders()
        
        if not orders:
            await query.edit_message_text(
                "📭 Заказов для удаления нет!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data='main_menu')
                ]])
            )
            return ConversationHandler.END
        
        message = "🗑️ **Удаление заказа**\n\n"
        message += "Список заказов:\n"
        for order in orders:
            order_id, name, item, time, _ = order
            message += f"#{order_id}: {name} - {item} (доставка: {time})\n"
        
        message += "\nВведите ID заказа для удаления:"
        
        await query.edit_message_text(message)
        return DELETE_ORDER
    
    async def confirm_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Подтверждение и удаление заказа"""
        try:
            order_id = int(update.message.text.strip())
            
           
            order = db.get_order(order_id)
            if not order:
                await update.message.reply_text(
                    f"❌ Заказ #{order_id} не найден!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
                    ]])
                )
                return ConversationHandler.END
            
            db.delete_order(order_id)
            
            await update.message.reply_text(
                f"✅ Заказ #{order_id} успешно удален!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
                ]])
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, введите корректный ID заказа (число)!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
                ]])
            )
        
        return ConversationHandler.END
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню"""
        query = update.callback_query
        await query.answer()
        await self.basket(update, context)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена операции"""
        await update.message.reply_text(
            "❌ Операция отменена.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛒 В корзину", callback_data='main_menu')
            ]])
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    def run(self):
        """Запуск бота"""
        print("Бот запущен...")
        self.application.run_polling(allowed_updates=Update.ALL_UPDATES)

if __name__ == '__main__':
    bot = OrderBot()
    bot.run()