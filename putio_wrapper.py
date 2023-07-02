import logging
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

class PutIo:
	base_url = "https://api.put.io/v2"
	token = os.getenv("USER_TOKEN")

	def _execute( self, http_type, api_path, request_body=None ):
		api_url = self.base_url + api_path
		response = None
		headers = {
			"Authorization": f"Bearer {self.token}"
			}
		if http_type == "get":
			response = requests.get(api_url, headers=headers)
		elif http_type == "post":
			response = requests.post(api_url, headers=headers, data=request_body)

		elif http_type == "put":
			response = requests.put(api_url, headers=headers, data=request_body)
		else:
			logging.error("Unknown request type"
			              f"\nhttp_type: {http_type}"
			              f"\napi_url: {api_url}")
		if response:
			return response.json()

	def printer( self, result_data: dict ):
		print(json.dumps(result_data, indent=4))

	def getFiles( self, parent_id=-1 ):
		path = f"/files/list?parent_id={parent_id}"
		return self._execute('get', path)

	def getDownloadUrl( self, file_id: int ):
		path = f"/files/{file_id}/url"
		return self._execute('get', path)

	def getTransferList( self ):
		path = f"/transfers/list"
		return self._execute('get', path)

	def startTransfer( self, magnet_link, cb_url=None, save_parent_id=None ):
		path = "/transfers/add"
		body = {"url": magnet_link, "callback_url": cb_url, 'save_parent_id': save_parent_id}
		return self._execute('post', path, body)

	def getTransferDetails( self, transfer_id ):
		path = f"/transfers/{transfer_id}"
		return self._execute('get', path)

	def deleteFiles( self, id_list ):
		path = f"/files/delete"
		body = {"file_ids": id_list}
		return self._execute('post', path, body)

	def removeTransfers( self, transfer_ids=None ):
		path = f"/transfers/clean"
		body = {"transfer_ids": transfer_ids}
		return self._execute('post', path, body)

