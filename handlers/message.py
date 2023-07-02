from telegram.ext import MessageHandler, filters
from controllers.torrent import start_download


def getMessageHandlers():
	return [
		MessageHandler(filters.Regex("(^magnet:\?xt=urn:btih:*)|(^http.*)"), start_download)
		]
