from telegram.ext import CallbackQueryHandler
from controllers.torrent import refresh_transfer

def getCallbackQueryHandlers():
    return [
        CallbackQueryHandler(pattern="^refresh_*", callback= refresh_transfer),
    ]