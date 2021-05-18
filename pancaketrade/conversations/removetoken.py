from typing import List, NamedTuple

from pancaketrade.network import Network
from pancaketrade.utils.config import Config
from pancaketrade.utils.db import remove_token
from pancaketrade.utils.generic import chat_message, check_chat_id
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler


class RemoveTokenResponses(NamedTuple):
    CONFIRM: int = 0
    TOKENCHOICE: int = 1


class RemoveTokenConversation:
    def __init__(self, parent, config: Config):
        self.parent = parent
        self.net: Network = parent.net
        self.config = config
        self.next = RemoveTokenResponses()
        self.handler = ConversationHandler(
            entry_points=[CommandHandler('removetoken', self.command_removetoken)],
            states={
                self.next.CONFIRM: [CallbackQueryHandler(self.command_removetoken_confirm)],
                self.next.TOKENCHOICE: [CallbackQueryHandler(self.command_removetoken_tokenchoice)],
            },
            fallbacks=[CommandHandler('cancelremovetoken', self.command_cancelremovetoken)],
            name='removetoken_conversation',
            conversation_timeout=60,
        )

    @check_chat_id
    def command_removetoken(self, update: Update, context: CallbackContext):
        assert update.message
        buttons: List[InlineKeyboardButton] = []
        for token in sorted(self.parent.watchers.values(), key=lambda token: token.symbol.lower()):
            buttons.append(InlineKeyboardButton(token.name, callback_data=token.address))
        buttons_layout = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]  # noqa: E203
        buttons_layout.append([InlineKeyboardButton('❌ Cancel', callback_data='cancel')])
        reply_markup = InlineKeyboardMarkup(buttons_layout)
        chat_message(
            update,
            context,
            text='Choose the token to remove from the list below.',
            reply_markup=reply_markup,
            edit=False,
        )
        return self.next.CONFIRM

    @check_chat_id
    def command_removetoken_confirm(self, update: Update, context: CallbackContext):
        assert update.callback_query and update.effective_chat
        query = update.callback_query
        # query.answer()
        if query.data == 'cancel':
            chat_message(update, context, text='⚠️ OK, I\'m cancelling this command.')
            return ConversationHandler.END
        assert query.data
        token = self.parent.watchers[query.data]
        chat_message(
            update,
            context,
            text=f'Are you sure you want to delete {token.name}?',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('✅ Confirm', callback_data=query.data),
                        InlineKeyboardButton('❌ Cancel', callback_data='cancel'),
                    ]
                ]
            ),
        )
        return self.next.TOKENCHOICE

    @check_chat_id
    def command_removetoken_tokenchoice(self, update: Update, context: CallbackContext):
        assert update.callback_query
        query = update.callback_query
        # query.answer()
        if query.data == 'cancel':
            chat_message(update, context, text='⚠️ OK, I\'m cancelling this command.')
            return ConversationHandler.END
        remove_token(self.parent.watchers[query.data].token_record)
        token_name = self.parent.watchers[query.data].name
        del self.parent.watchers[query.data]
        chat_message(update, context, text=f'✅ Alright, the token <b>"{token_name}"</b> was removed.')
        return ConversationHandler.END

    @check_chat_id
    def command_cancelremovetoken(self, update: Update, context: CallbackContext):
        assert update.effective_chat
        chat_message(update, context, text='⚠️ OK, I\'m cancelling this command.')
        return ConversationHandler.END
