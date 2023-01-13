from channels.generic.websocket import JsonWebsocketConsumer
import app.simple_app.actions as actions


class ExampleConsumer(JsonWebsocketConsumer):

	def connect(self):
		self.accept()
		# Make sessions task list
		if "tasks" not in self.scope['session']:
			self.scope['session']['tasks'] = []
			self.scope['session'].save()

	def disconnect(self, close_code):
		pass 

	def receive_json(self, data_received):

		"""
            Event when data is received
            All information will arrive in 2 variables:
            "action", with the action to be taken
            "data" with the information
		"""
		#Get data
		data = data_received['data']

		# Depending on the action we will do one task or
		# another.
		match data_received['action']:
			case "change page":
				actions.send_page(self, data['page'])

			case 'Add lap':
				actions.add_lap(self)

			case "Add task":
				actions.add_task(self, data)

			case "login":
				actions.action_signup(self, data)


	def send_html(self, event):
		"""Event: Send html to client"""
		data = {
			'selector': event['selector'],
			'html': event['html'],
			'append': 'append' in event and event['append'],
			'url': event['url'] if "url" in event else "",
		}

		self.send_json(data)
