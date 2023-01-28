class Shablon:
	def _init_(self):
		pass

	def bot_shablon(self):
		return '''from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api, json
from config import tok

vk_session = vk_api.VkApi(token = tok)
longpoll = VkLongPoll(vk_session)

class User:
	def _init_(self, id, mode):
		self.id = id

def get_keyboard(buts):
	nb = []
	for i in range(len(buts[i])):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'зеленый': 'positive', 'красный':'negative', 'синий':'ptimary'}(buts[i][k][1])
			nb[i][k] = {"action": {"type": "text", "payload": "{\"button\":\"" + "1"+ "\"}", "label": f"{text}"}, "color": f"{color}"}
	first_keyboard = {'one_time':False, 'buttons': nb, 'inline': False}
	first_keyboard = json.dumps(first_keyboard, ensure_ascil=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard

def sender(id, text, key):
	vk_session.method('message.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key})

clear_key = get_keyboard(
	[]
)

users = []

for event in longpoll.listen():
	if event.type = VkEnentType.MESSAGE_NEW:
		if event.to_me:

			id = event.user_id
			msg = event.text.lower()

			sender(id, msg.upper(), clear_key)'''

	def cpp_shablon(self):
		return '''#include <iostream>
using namespace std:

int main(){
	
	return 0;
}'''