import time, ctypes, webbrowser as web, pygame
from fuzzywuzzy.fuzz import ratio as rat
from random import choice
from colorama import *
from os import system, getpid, listdir
from datetime import datetime
from psutil import virtual_memory as ozu
from GoogleNews import GoogleNews

from bot_shablons import Shablon
from remind_class import Reminder
from creator import File_creator

class VirtualAssistent(Shablon, Reminder, File_creator):

	def __init__(self):
		pass


	def surprise(self):
		vals = ['Я тоже удивлена', 'Мне тоже нравится', 'Мне тоже кажется, что это классно']
		self.add_phrases(choice(vals))


	def go_to_page(self, task):
		if task.startswith(('на ', 'в ', 'открой ')):
			task = task.replace('на ', '', 1).replace('в ', '', 1).replace('открой ', '', 1).replace('  ', ' ').strip()

		vals = {
			 'https://student.knastu.ru/account' : ('расписание', 'сайт кнагу', 'сайт канаву'),
			 'https://www.google.com/adsense' : ('adsense'),
			 'https://www.youtube.com/channel/UCYdNEPcVLdPOiEL9BXVMCrQ' : ('мой канал', 'канал', 'youtube'),
			 'https://github.com/' : ('гитхаб', 'гит', 'репозитории'),
			 'https://vk.com/feed' : ('vk', 'вконтакте')
		}

		koof = 0
		e_link = ''
		for link in vals:
			for val in vals[link]:

				if rat(val, task) == 100:
					e_link = link
					break

				elif (rat(val,task) > 80) and (rat(val, task) > koof):
					e_link = link
					koof = rat(val, task)

		if e_link:
			self.engine.Speak(choice(['Сейчас зайду', 'Захожу', 'Открываю']))
			web.open(e_link)


	def comparison(self, word, options, per = 70):
		flag = 0
		for var in options:
			if rat(var, word) > per:
				flag =1
				return True
				break
		if flag == 0:
			return False


	def create_news(self, time, theme):#парсинг новостей
		googlenews = GoogleNews()
		googlenews.set_lang('ru')
		googlenews.set_period(time)
		googlenews.search(theme)
		googlenews.get_page(1)
		ans = googlenews.get_texts()
		return choice(ans)


	def show_news(self, task):#рассказать новости
		time = '10d'; theme = ''
		if ('на сегодня' in task) or ('сегодня' in task and 'нового' in task):
			time = '1d'
		task = f' {task} '
		for val in (' новости ', ' какие новости ', ' новости на сегодня ', ' что нового ', ' есть новости ',
			' есть ', ' на тему ', ' сегодня ', ' неделю '):
			task = task.replace(val, ' ').replace('  ', ' ')

		for val in ('новости', 'какие новости', 'новости на сегодня' , 'что нового', 'есть новости',
		'есть', 'на тему', 'неделю', 'сегодня'):
			task = task.replace(val, ' ').replace('  ', ' ')

		for i in ('какие на', 'на какие'):
			if len(task.replace(i, '').strip()) < 3:
				task = task.replace(i, ' ').replace('  ', ' ').strip()

		task = f'новости {task}'.replace('  ', ' ')
		self.add_phrases(choice(['Сейчас поищем', 'нужно поискать']))
		self.talk()
		self.add_phrases(self.create_news(time, task))


	def web_talk(self, task):#рассказывает то, что найдет по запросу
		#task = необработанный запрос
		pass


	def check_get_ideas(self, task):
		vals = ['как думаешь ', 'что думаешь ']
		for val in vals:
			if task.startswith(val):
				task = task.replace(val, '', 1).strip()
		vals = ['сегодня', 'завтра', 'вечером', 'утром', 'днём', 'выходных', 'на ', 'в ']
		task = task.split()
		for val in vals:
			for word in task:
				if rat(word, val) > 80:
					del task[task.index(word)]
		task = ' '.join(task)
		for val in vals:
			if val in task:
				task = task.replace(val, '').replace('  ', ' ').strip()
		vals = ('чем можно заняться', 'чем заняться', 'что поделать', 'как убить время', 'мне скучно', 'чем позаниматься',
			'как провести время' , 'что можно поделать', 'чем предлагаешь заняться')

		flag = 0

		for i in range(len(task.split())):
			if (task.split()[i] == 'чем'):
				for k in range(i+1, len(task.split())):
					if self.comparison(task.split()[k], ['заняться']) and (k-i < 4):
						flag = 1
						break

		for val in vals:
			if (((rat(val, task) > 70) or (task.startswith(val))) and not(task in ['что делаешь', 'чем занимаешься'])):
				flag = 1
				break

		return flag


	def on_music(self):
		self.add_phrases(choice(['Приятного прослушивания', 'Включаю подборку песен']))
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.load(f'{self.music_path}/{listdir(self.music_path)[0]}')
		for music in [f'{self.music_path}/{x}' for x in listdir(self.music_path)[1:] if '.' in x]:
			pygame.mixer.music.queue(music)
		pygame.mixer.music.play(-1)


	def off_music(self):
		pygame.mixer.music.stop()


	def get_ideas(self, task):
		vals = ['как думаешь', 'что думаешь']
		for val in vals:
			if task.startswith(val):
				task = task.replace(val, '', 1).strip()
		vals = ['сегодня', 'завтра', 'вечером', 'утром', 'днём', 'выходных', 'на', 'в']
		task = task.split()
		for val in vals:
			for word in task:
				if rat(word, val) > 80:
					del task[task.index(word)]
		task = ' '.join(task)

		ans = ''
		for teg in self.ext(task):
			for val in self.ideas:
				if rat(teg.normalized, val) > 70:
					ans = choice(self.ideas[val])
					break

		if ans == '':
			ans = choice(self.ideas[choice([x for x in self.ideas])])

		ans = f"{choice(['Я думаю, вам стоит', 'Можете попробовать', 'Как вариант', 'Попробуйте', 'Вам стоит', 'Не плохо было бы'])} {ans}"
		self.add_phrases(ans)


	def search_on_map(self, task):
		for val in ['находится', 'расположен', 'где']:
			if rat(task.split()[0], val) > 70:
				task = ' '.join(task.split()[1:])
			task = task.replace(val, '').replace('  ', ' ')
		for val in ['мне', 'нам', 'всем', 'им']:
			if rat(task.split()[0], val) > 70:
				task = ' '.join(task.split()[1:])
			task = task.replace(val, '').replace('  ', ' ')
		task = task.replace(val, '').replace('  ', ' ').strip()
		web.open(f'https://www.google.ru/maps/search/{task}')
		self.engine.Speak(choice(['Сейчас найдём', 'надеюсь, вы не собираетесь уходить', 'если вы уйдете, мне будет скучно']))


	def talk(self):

		count = 0
		phrase = ''

		for var in ["здравствуйте", "доброе утро", "добрый день", "добрый вечер", "доброй ночи"]:
			if var in self.phrases:
				if count == 0:
					phrase = var
					for i in range(self.phrases.count(var)):
						del self.phrases[self.phrases.index(var)]
					count += 1
				else:
					for i in range(self.phrases.count(var)):
						del self.phrases[self.phrases.index(var)]
		if phrase:
			self.phrases.insert(0, phrase)

		for text in self.phrases:
			self.engine.Speak(text)
		self.phrases = []


	def weather(self):
		w = self.observation.weather
		status = w.detailed_status
		temp = str(int(w.temperature('celsius')['temp'])).replace('-', 'минус')

		ok = {
			0: 'ов', 1: '', 2: 'а', 3: 'а', 4: 'а', 5: 'ов', 6: 'ов', 7: 'ов', 8: 'ов', 9: 'ов', 10: 'ов',
			11: 'ов', 12: 'ов', 13: 'ов', 14: 'ов', 15: 'ов', 16: 'ов', 17: 'ов', 18: 'ов', 19: 'ов', 20: 'ов',
			21: '', 22: 'а', 23: 'а', 24: 'а', 25: 'ов', 26: 'ов', 27: 'ов', 28: 'ов', 29: 'ов', 30: 'ов',
			31: '', 32: 'а', 33: 'а', 34: 'а', 35: 'ов', 36: 'ов', 37: 'ов', 38: 'ов', 39: 'ов', 40: 'ов',
			41: '', 42: 'а', 43: 'а', 44: 'а'
		}

		a = choice(['городе', ""])
		end = ok[int(temp.replace("минус", ''))]

		self.add_phrases(f'В {a} сейчас {status}. На улице {temp} градус{end} по цельсию.')


	def add_phrases(self, text):
		self.last_phrase = text
		self.phrases.append(text)


	def first_ans(self):
		vals = ('я вас слушаю', 'да-да', 'я здесь')
		self.add_phrases(choice(vals))


	def well_done(self):
		vals = [
			"Спасибо, так приятно!",
			"Вы тоже ничего...", "Да, я такая!", "Я тоже так думаю."
		]
		self.add_phrases(choice(vals))


	def bye(self):
		self.engine.Speak(choice(['До свидания']))
		system(f'taskkill /IM {getpid()} /F')


	def hello(self):
		time = int(datetime.now().hour)
		if time in (6,7,8,9,10,11,12):
			self.add_phrases(choice(["доброе утро", "здравствуйте"]))
		elif time in (13,14,15,16,17,18):
			self.add_phrases(choice(["добрый день", "здравствуйте"]))
		elif time in (19,20,21,22,23):
			self.add_phrases(choice(["добрый вечер", "здравствуйте"]))
		else:
			self.add_phrases(choice(["доброй ночи", "здравствуйте"]))


	def greet(self):
		vals = [
			'Здравствуйте, рада вас видеть', 'Всем привет, я Сара',
			'Доброго времени суток всем присутствующим'
		]
		self.add_phrases(choice(vals))


	def how_are_you(self):
		vals = [
			"Как у укропа - пучком все!", "Хорошо дела идут, только мимо",
			"Дела через полосочку  в клеточку у меня", "Мухам бы точно понравилось"
		]
		self.add_phrases(choice(vals))


	def what_doing(self):
		vals = ["Именно сейчас? Отвечаю Вам на поставленный вопрос", "Танцую джаз",
			"Помогаю президенту урегулировать положение в нашей стране", "Сушу сухари",
			"Стреляю из самого мощного автомата в мире, скорее магнись, чтобы тебя не зацепило",
			"Отмечаю день города в Кейптауне", "А ты угадай с трех раз! Догадаешься с меня приз.",
			"А почему ты об этом спрашиваешь каждый день?",
			"Это повод поговорить, или на самом деле интересно?", "Думаю о будущем общества",
			"Кота разговаривать учу, чтобы он вместо меня отвечал на такие вопросы"]
		self.add_phrases(choice(vals))


	def thanks(self):
		vals = ['Рада была вам помочь', 'Обращайтесь в любое время', 'Всегда к вашим услугам', 'Рада заслужить ваше доверие']
		self.add_phrases(choice(vals))


	def shut_down(self):
		self.engine.Speak('Вы уверены, что хотит выключить компьютер?')
		answer = ''

		while answer == '':
			answer = self.listen()

			if answer:
				for val in ('да', 'да выключай', 'выключай', 'да уверен'):
					if rat(val, answer) > 90:
						self.off_light()
						system('shutdown /s /f /t 10')
						break


	def lock(self):
		ctypes.windll.user32.LockWorkStation()


	def open_youtube(self):
		web.open(f'https://www.youtube.com/')


	def day_of_week(self):
		weekdays = {
			0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'
		}
		self.add_phrases(f'Сегодня {weekdays[datetime.today().weekday()]}')


	def time_now(self):
		now = datetime.now()
		self.add_phrases(f'Сейчас {now.hour} {now.minute}')


	def date_is_today(self):
		self.add_phrases(f'Сегодня {self.strs[datetime.now().day]} число')


	def repeat(self):
		self.add_phrases(self.last_phrase)


	def web_search(self, task):
		mode = 'web'

		for i in range(len(task.split())-1):
			if (rat(task.split()[i], 'найди') > 80) and (rat(task.split()[i+1], 'видео') > 80):
				task = task.split()
				del task[i]
				del task[i+1]
				task = ' '.join(task)
				mode = 'tube'
				break

		for var in ('найди в youtube', 'найди на youtube', 'найди видео на тему', 'найди видео на канале', 'на канале', 'видео'):
			if var in task:
				mode = 'tube'
				task = task.replace(var, '').replace('  ', ' ').strip()

		if mode == 'web':
			for var in ['найди ка ', 'поищи ка ', 'найди', 'поищи']:
				task = task.replace(var, '').replace('  ', ' ').strip()

			if task:
				self.add_phrases(choice(['Уже ищу', 'Сейчас найду', 'Сейчас поищем']))
				if float(ozu().percent) <= 95:
					web.open(f'https://www.google.com/search?btnG=1&q={task}')
				else:
					self.add_phrases(choice([
						'Компьютер сильно нагружен, не стоит открывать новые вкладки в браузере, я могу рассказать вам необходимую информацию. Прочитать?',
						'Компьютер сильно нагружен, давайте я лучше прочитаю?']))

					answer = ''
					while not(answer):
						answer = self.listen()

					flag = 0
					for var in ('нет', 'не нужно', 'не надо'):
						if rat(var, answer) > 70:
							self.add_phrases('Хорошо')
							flag = 1
							break

					if flag == 0:
						for var in ('да', 'давай', 'можно', 'рассказывай', 'расскажи', 'читай', 'прочитай'):
							if rat(var, answer) > 70:
								self.web_talk(task)
								break
		else:
			if float(ozu().percent) <= 95:
				for var in ('видео про ', 'видео о ', 'видео', 'на канале', 'канале'):
					if var in task:
						task = task.replace(var, '').replace('  ', ' ').strip()
				self.add_phrases(choice(['Уже ищу', 'Сейчас найду', 'Сейчас поищем']))
				web.open(f'https://www.youtube.com/results?search_query={task}')
			else:
				self.add_phrases(choice(['Не стоит открывать новые вкладки, компьютер сильно нагружен', 'Если я открою youtube, компьютер может зависнуть']))


	def connect(self):
		log = system('MODE COM3: BAUD=9600 DATA=8 STOP=1 PARITY=N to=off xon=iff odsr=off octs=off rts=off idsr=off dtr=off')
		system('cls')
		if log == -1:
			self.add_phrases(choice(self.ard_error_msgs))


	def on_light(self):
		log = system('echo 1 > COM3')
		system('cls')
		if log == -1:
			self.add_phrases(choice(self.ard_error_msgs))


	def off_light(self):
		log = system('echo 2 > COM3')
		system('cls')
		if log == -1:
			self.add_phrases(choice(self.ard_error_msgs))


	def error_log(self, error_code):
		try:
			with open('logs.txt', 'a', encoding = 'utf-8') as file:
				my_data = str(datetime.now())
				index = my_data.index('.')
				file.write(f'{my_data[0:index]} : {error_code}\n')
				file.close()
		except Exception as e:
			file = open('logs.txt', 'w', encoding = 'utf-8')
			file.close()


	def listen(self):
		system('cls')
		text = ''
		print(choice((Fore.GREEN, Fore.WHITE, Fore.YELLOW)) + 'Я вас слушаю: ')
		with self.m as self.sourse:
			self.r.adjust_for_ambient_noise(self.sourse)
		while text == '':
			with self.m as self.sourse:
				audio = self.r.listen(self.sourse)
				try:
					text = (self.r.recognize_google(audio, language = 'ru_RU')).lower()
					print('Распознано: '+ text)
				except:
					pass
		if text in ('эй', 'сара', 'ты здесь', 'ты тут', 'слышь', 'слышишь', 'сара ты тут', 'сара ты здесь'):
			self.first_ans()
			return ''
		else:
			return( text )


	def search_exe_function(self, task):
		coef = 0
		ans = None
		for mas in self.cmds:
			if mas == ('что делаешь', 'чем занимаешься'):
				for var in mas:
					if (coef < rat(task, var) > 99):
						ans = mas
						coef = rat(task, var)
			else:
				for var in mas:
					if (coef < rat(task, var) > 70):
						ans = mas
						coef = rat(task, var)
		if ans:
			return ans
		else:
			return ''


	def delete_doubles2(self, ans):
		last = ''
		tasks = ans
		ans = []

		if ('поздоровайся', 'поприветствуй всех', 'поздоровайся со всеми') in tasks:
			for i in range(tasks.count(('здаров', 'привет', 'здравствуй'))):
				del tasks[tasks.index(('здаров', 'привет', 'здравствуй'))]
			del tasks[tasks.index(('поздоровайся', 'поприветствуй всех', 'поздоровайся со всеми'))]
			tasks.insert(0, ('поздоровайся', 'поприветствуй всех', 'поздоровайся со всеми'))

		for task in tasks:
			if task != last:
				ans.append(task)
				last = task
			else:
				pass
		return ans

