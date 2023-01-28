from random import choice
from datetime import datetime, timedelta
from os import system

class Reminder:

	def write_remind(self, line): #не записывает
		print(f'LINE: {type(line)} = {line}')
		with open('reminds.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'{line}\n')


	def check_time(self, num):
		if int(datetime.now().strftime("%H")) < num:
			hours = num - int(datetime.now().strftime("%H"))
			minutes = 0 - int(datetime.now().strftime("%H"))
			kk = datetime.now() + timedelta(hours = hours, minutes = minutes)
		else:
			hours = num + (24 - int(datetime.now().strftime("%H")))
			minutes = 0 -int(datetime.now().strftime("%H"))
			kk = datetime.now() + timedelta(hours = hours, minutes = minutes)
		return str(kk)


	def create_remind(self, task):

		self.engine.Speak(choice['Работа с напоминаниями не налажела, не уверена, что смогу напомнить',
								 'Предупреждаю, напоминания работают некорректно'])
		task = task.strip()

		if task.startswith('через '):
			task = task.replace('через ', '')
			if ('часов' in task) or ('часа' in task):
				if 'часов' in task:
					task = task.split('часов')
				else:
					task = task.split('часа')

				for i in range(len(task)):
					task[i] = task[i].strip()

				out_date = datetime.now() + timedelta(hours = int(task[0]))
				out_date = f'{str(out_date)} {task[1]}'


		elif task.startswith('вечером '):
			task = task.replace('вечером ', '')
			out_date = f'{self.check_time(19)} {task}'


		elif task.startswith('днём '):
			task = task.replace('днём ', '')
			out_date = f'{self.check_time(15)} {task}'


		elif task.startswith('в '):
			pass


		elif task.startswith('завтра '):
			pass


		self.write_remind(str(out_date))
		self.add_phrases(choice(['Хорошо, я напомню', 'Постараюсь не забыть', 'Хорошо, я всё записала!']))