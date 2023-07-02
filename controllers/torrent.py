from putio_wrapper import PutIo
from telegram.ext import ContextTypes
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import humanize


async def start_download( update: Update, context: ContextTypes.DEFAULT_TYPE ):
	to_download_link = update.effective_message.text
	obj = PutIo()
	result = obj.startTransfer(to_download_link)
	if result.get("status") == "OK":
		tr_id = result["transfer"]["id"]

		keyboard = InlineKeyboardMarkup([
			[InlineKeyboardButton('Refresh', callback_data=f"refresh_{tr_id}")]
			])

		await update.effective_message.reply_html(
			f'Status : <b>{result["transfer"]["status"]}</b>',
			reply_markup=keyboard)

	else:
		if result.get("error_type") == "TRANSFER_ALREADY_ADDED":
			existing_tr_id = result["extra"]["existing_id"]
			keyboard = InlineKeyboardMarkup([
				[InlineKeyboardButton('Refresh', callback_data=f"refresh_{existing_tr_id}")]
				])
			await update.effective_message.reply_html(
				f'Status : <b>Already added</b>',
				reply_markup=keyboard)


async def refresh_transfer( update: Update, context: ContextTypes.DEFAULT_TYPE ):
	query = update.callback_query
	await query.answer("Refreshing...")
	data = query.data
	transfer_id = data.split("_")[1]
	keyboard = InlineKeyboardMarkup([
		[InlineKeyboardButton('Refresh', callback_data=f"refresh_{transfer_id}")]
		])

	obj = PutIo()
	result = obj.getTransferDetails(transfer_id)

	if result.get("status") == "OK":
		file_id = result["transfer"]["file_id"]
		total_size = result["transfer"]["size"]
		downloaded = result["transfer"]["downloaded"] if result["transfer"]["downloaded"] is not None else 0

		if total_size is None:
			preparing_text = f'Updated Status : <b>{result["transfer"]["status"]}</b>'
			await update.callback_query.edit_message_text(
				text=preparing_text,
				parse_mode="HTML",
				reply_markup=keyboard)
			return

		if file_id is None:
			downloading_text = f'Completed : <b>{humanize.naturalsize(downloaded)}</b>/{humanize.naturalsize(total_size)}'
			await update.callback_query.edit_message_text(
				text=downloading_text,
				parse_mode="HTML",
				reply_markup=keyboard)
		else:
			after_downloading_text = f'Name : <b>{result["transfer"]["name"]}</b>\nSize : <b>{humanize.naturalsize(total_size)}</b>'
			url_result = obj.getDownloadUrl(file_id)
			if url_result.get("status") == "OK":
				await update.callback_query.edit_message_text(
					text=after_downloading_text,
					reply_markup=InlineKeyboardMarkup([
						[InlineKeyboardButton('Download Link', url_result["url"])]
						]),
					parse_mode="HTML")

			else:
				await update.callback_query.edit_message_text("Something went wrong!", reply_markup=keyboard)

	else:
		await update.callback_query.edit_message_text("Something went wrong!", reply_markup=keyboard)
