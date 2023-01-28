from fuzzywuzzy.fuzz import ratio as rat
from random import choice
from os import getcwd, chdir, mkdir

class File_creator:

	def create_new_project(self, task):
		save_task = task
		nows = ['новый', 'новым', 'очередной', 'очередным', 'создай', 'создадим', 'нового']
		n_task = task.split()
		time = 'old'
		lang = ''
		tz = ''
		cpp_theme = ['си плюс', 'плюсах', 'arduino']
		python_theme = ['python', 'питоне', 'питона', 'питон', 'на питоне']
		bot_theme = ['vk бота', 'бота vk', 'с ботом', 'бота']
		for val in nows:
			for i in range(len(n_task)):
				if rat(val, n_task[i]) > 70:
					time = 'new'
					del n_task[i]
					break

		task = ' '.join(n_task).replace('  ', ' ').strip()
		dels = ['давай создадим ', 'поработаем над ', 'давай ', 'поработаем ', 'создай ', 
		'открой ', 'проект ', 'на ', 'для ', 'шаблон ', 'наброски ', 
		'с названием ', 'назови его ', 'под названием ', 'нового']

		for nd in dels:
			if nd in task:
				task = task.replace(nd, '')
		task = task.split()
		for nd in dels:
			for i in range(len(task)):
				if rat(nd,task[i]) > 75:
					task[i] = ''

		task = ' '.join(task).replace('  ', ' ').strip()

		if not(task): task = 'standart'

		if time == 'new':
			if task != 'standart':

				for val in cpp_theme:
					if (val in task) or (self.comparison(val, task.split()) or self.comparison(val, task.split())):
						lang = 'cpp'
						task = task.replace(val, '').replace('  ', ' ').strip()
						break

				for val in python_theme:
					if (val in task) or (self.comparison(val, task.split())):
						lang = 'python'
						task = task.replace(val, '').replace('  ', ' ').strip()
						break

				for val in bot_theme:
					if (val in task) or (self.comparison(val, task.split())):
						lang = 'python'
						tz = 'bot'
						task = task.replace(val, '').replace('  ', ' ').replace('бота', '').replace('бот', '').strip()
						break

				if not(lang in ['cpp', 'python']):
					self.engine.Speak(choice(['На каком языке будет проект?', 'На чём будете писать проект?']))
					t_lang = self.listen().replace('на', '').replace('давай', '').replace('можно', '').strip()
					for nd in dels:
						for i in range(len(t_lang)):
							if rat(nd, t_lang[i]) > 80:
								t_lang[i] = ''
					for val in cpp_theme:
						if (val in t_lang) or (self.comparison(val, t_lang.split())):
							lang = 'cpp'
							break
					for val in python_theme:
						if (val in t_lang) or (self.comparison(val, t_lang.split())):
							lang = 'python'
							break

			else:
				self.engine.Speak(choice(['Как назвать этот проект?', 'Вы уже придумали название проекта?', 'Как вы хотите назвать проект?']))

				while not(task) or (task == 'standart'):
					name = self.listen()
					for i in ['назови', 'назови его', 'просто', 'давай назовём', 'давай', 'да', 'придумал', 'бота', 'нового']:
						name = name.replace(i, '').replace('  ', ' ').strip()
					if name:
						task = name.replace(' ', '_')

		elif time == 'old':
			pass#наверное не будет

		for i in ['python', 'питоне', 'питона', 'vk бота', 'бота vk', 'с ботом', 'бота', 'си плюс', 'плюсах', 'arduino', 'с названием', 'под названием']:
			task = task.replace(i, '').replace('  ', ' ').strip()

		if not(task):
			self.engine.Speak(choice(['Как назвать этот проект?', 'Вы уже придумали название проекта?', 'Как вы хотите назвать проект?']))

			while not(task):
				name = self.listen()
				for i in ['назови', 'назови его', 'просто', 'давай назовём', 'давай', 'да', 'придумал', 'бота', 'нового']:
					name = name.replace(i, '').replace('   ', ' ').strip()
				if name:
					task = name.replace(' ', '_')

		for i in ['под ', 'с ', 'под_', 'с_', 'с_названием', 'под_названием']:
			if task.startswith(i):
				task = task.replace(i, '', 1)
			task = task.strip()

		if not(lang in ['cpp', 'python']):
			self.engine.Speak(choice(['На каком языке будет проект?', 'На чём будете писать проект?']))
			t_lang = self.listen().replace('на ', '').replace('давай ', '').replace('можно ', '').strip()
			for nd in dels:
				for i in range(len(t_lang)):
					if rat(nd, t_lang[i]) > 80:
						t_lang[i] = ''
			for val in cpp_theme:
				if (val in t_lang) or (self.comparison(val, t_lang.split())):
					lang = 'cpp'
					break
			for val in python_theme:
				if (val in t_lang) or (self.comparison(val, t_lang.split())):
					lang = 'python'
					break

		en = {'а' : 'a', 'м' : 'm',
			'б' : 'b', 'н' : 'n',  'в' : 'v', 'о' : 'o',  'г' : 'g', 'п' : 'p',  'д' : 'd', 'р' : 'r',
			'е' : 'e', 'с' : 's',  'ё' : 'yo', 'т' : 't',  'ж' : 'g', 'у' : 'u',  'з' : 'z', 'ф' : 'f',
			'и' : 'i', 'х' : 'h',  'й' : 'y', 'ц' : 'tc',  'к' : 'k', 'ч' : 'ch',  'л' : 'l', 'ш' : 'sh',
			'щ' : 'sh', 'ы' : 'i',  'ъ' : '', 'ь' : '',  'э' : 'e', 'я' : 'ya',  'ю' : 'yu', ' ' : ' '
		}

		if (time == 'new') and (lang) and (task):
			try:
				for i in ['с ', 'с_', 'с ', 'с_', 'с_названием']:
					if task.startswith(i):
						task = task.replace(i, '', 1)
				k = ''
				print(task)
				for i in range(len(task)):
					if not(task[i].isdigit()):
						try:
							k = f'{k}{en[task[i]]}'
						except:
							k = f'{k}{task[i]}'
					else:
						k = f'{k}{task[i]}'

				task = k
				now_dir = getcwd()
				#input(now_dir)
				chdir(self.projects_dir_path)#перешли в projects
				mkdir(task.replace(' ', '_'))#создали папку с проектом
				chdir(f'{self.projects_dir_path}/{task.replace(" ", "_")}')#перешли в папку с проектом

				mkdir('backups')
				mkdir('tests')
				mkdir('main')
				mkdir('main')

				if lang == 'python':
					with open('main.py', 'w', encoding = 'utf-8') as file:
						if tz == 'bot':
							file.write(self.bot_shablon())
						else:
							pass

				elif lang == 'cpp':
					with open('main.py', 'w', encoding = 'utf-8') as file:
						file.write(self.cpp_chablon())

				chdir(now_dir)
				self.add_phrases(choice(['Уже создала!', 'Новый проект создан!']))

			except Exception as e:
				self.error_log(e)
				self.add_phrases('Мне не удалось создать проект')

		else:
			print(f'{save_task}\n\t{time}\n\r{lang}\n\t{task}')
			self.add_phrases(choice(['Я не поняла, что нужно созать!', 'Не уверена, что правильно всё поняла']))
