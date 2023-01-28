from fuzzywuzzy.fuzz import ratio as rat
from random import choice

class cmd_reccognizer:

	def __init__(self):
		pass

	def clear_cmd(self, global_task):

		for val in ['пожалуйста', 'не могла бы ты', 'прошу']:
			global_task = global_task.replace(val, '').strip()

		def clear_cmd3(k):
			tasks = []
			task = ''
			if len(k.split()) < 2:
				return [k]
			elif k != '': 
				k = k.split()
				for i in range(-1, len(k)-2):
					if (i+1 == len(k)-2):
						if k[i+2]:
							task = f'{task} {k[i+1]} {k[i+2]}'
						else:
							task = f'{task} {k[i+1]}'
						tasks.append(task.strip())
					else:
						for j in range(len(self.keywords)):
							if (rat(k[i+1], self.keywords[j]) > 80):
								tasks.append(task.strip())
								task = ''
								break
						if k[i+2]:
							task = f'{task} {k[i+1]} {k[i+2]}'
						else:
							task = f'{task} {k[i+1]}'
				for i in range(len(tasks)):
					task = tasks[i].split()
					for dl in ('уйди', 'свали'):
						if task:
							if rat(task[-1], dl) > 70:
								tasks[i] = (tasks[i].replace(task[-1], '')).strip()
								tasks.append('не мешай')
					if task:
						if rat(task[-1], 'мешай') > 80:
							if rat(task[-2], 'не') > 80:
								tasks[i] = (tasks[i].replace(task[-1], '')).strip()
								tasks[i] = (tasks[i].replace(task[-2], '')).strip()
								tasks.append('не мешай')
				for i in range(len(tasks)):
					if tasks[i].endswith(' и'):
						ntask = tasks[i].split()
						del ntask[len(ntask)-1]
						tasks[i] = (' '.join(ntask))
				for i in range(len(tasks)):
					if tasks[i].split():
						if rat(tasks[i].split()[-1], 'потом') > 80:
							ntask = tasks[i].split()
							del ntask[-1]
							tasks[i] = ' '.join(ntask)
			if (tasks and k):
				tasks[-1]=f'{tasks[-1]} {k[-1]}'
			return list(filter(None, tasks))

		def main(k):
			new_list = clear_cmd3(k)
			taskss = []
			for task in new_list:
				var = clear_cmd3(task)
				for i in var:
					taskss.append(i)

			new_list = []
			for task in taskss:
				var = clear_cmd3(task)
				for i in var:
					new_list.append(i)


			taskss = []
			for task in new_list:
				task = task.split()
				if len(task) == 1:
					taskss.append(" ".join(task))
				else:
					n_task = ''
					for var in range(len(task)):
						if (task[var] in self.keywords):
							taskss.append(n_task.strip())
							n_task = task[var]
						elif (var == len(task)-1):
							n_task = f'{n_task} {task[var]}'
							taskss.append(n_task.strip())
						else:
							n_task = f'{n_task} {task[var]}'
			return [value for value in taskss if value]

		def delete_doubles(ans):
			for task in range(len(ans)):
				wars = []
				last = ''
				var = ans(task).split()
				for word in var:
					if word != last:
						wars.append(word)
					last = word
				ans[task] = ' '.join(wars)
			return ans

		def task_interpreter(ans):
			def get_pairs(task):
				ans = []
				flag = 0
				for double in self.double_keys:
					pairs = [' '.join(double).strip(), ' '.join(double[::-1]).strip()]
					for pair in pairs:
						if pair in task:#если пара есть в запросе
							flag = 1
							var = task.replace(pair, '').strip()

							if task.startswith(pair):
								ans.append(pair)
							elif task.endswith(pair):
								ans.append([var, pair])

				if flag == 0:
					ans.append(task)

				return ans

			def rearkh(mas):
				def rearkh_cycle(ans):
					nans = ans
					ans = []
					for val in nans:
						if type(val) == list:
							for i in val:
								ans.append(i)  
						else:
							ans.append(val)

					return ans

				def check(mas):
					flag = 0
					for val in mas:
						if type(val) == list:
							flag = 1
					return flag

				while check(mas):
					mas = rearkh_cycle(mas)

				return mas

			for i in range(len(ans)):
				ans[i] = get_pairs(ans[i])

			return rearkh(ans)

		ans = delete_doubles(main(global_task))
		ans = self.delete_doubles2(task_interpreter(ans))

		del self.keywords[self.keywords.index('поздоровайся')]
		n_ans = [x for x in ans if not(x in self.keywords)]
		self.keywords.append('поздоровайся')

		for var1 in ('поздоровайся', 'поприветствуй всех', 'поздоровайся со всеми'):
			if var1 in n_ans:
				for var2 in ('здаров', 'привет', 'здравствуй'):
					if var2 in n_ans:
						del n_ans[n_ans.index(var2)]

		ans = []
		for task in n_ans:
			flag = 0
			if task.endswith(' и'):
				task = (task[::-1].replace('и ', '', 1))[::-1]
			if task.startswith('и '):
				task = task.replace('и ', '', 1)

			for i in [' сначала ', ' и ',' потом ', 'сделай', 'ладно', 'найди']:

				if ((i in task) and (not (task.split()[0] in ['найди', 'расскажи', 'добавь', 'удали']))):
					if 'найди' in task:
						if task.split().index('найди') > 0:
							t1 = ' '.join(task.split()[0:task.split().index('найди')])
							t2 = ' '.join(task.split()[task.split().index('найди'):])
							if t1.startswith('и '):
								t1 = t1.replace('и ', '').split()[::-1]
							if t1.endswith('и '):
								t1 = t1[::-1].replace('и ', '').strip()[::-1]
							if t2.startswith('и '):
								t2 = t2.replace('и ', '').split()[::-1]
							if t2.endswith('и '):
								t2 = t2[::-1].replace('и ', '').strip()[::-1]
							ans.append(t1)
							ans.append(t2)
							flag = 1
					if not(task.split()[1] in ['с', 'кто', 'какой', 'как', 'когда', 'где', 'почему', 'от', 'для']):
						task = task.replace(i, ' ').strip().replace('  ', '')
				if rat(task, 'сара') < 70:
					task = task.replace('сара', ' ').strip()

			n_task = task.strip().replace('  ', ' ').split()
			if len(n_task) > 1:
				for name in ('сара', 'саров', 'старая', 'стара'):
					if name in n_task:
						task = task.replace(name, '')

			if flag == 0:
				ans.append(task.strip().replace(' ', ''))

		for task in range(len(ans)):
			j_task = ans[task]
			while ('спасибо' in ans[task]) and (len(ans[task].split()) > 1):
				ans[task] = ans[task].split()
				for var in ["большое", "огромное", "конечно", "тебе"]:
					for i in range(len(ans[task])-1):
						if ans[task][i] == 'спасибо':
							if ans[task][i+1] == var:
								del ans[task][i+1]
							if i > 0:
								if ans[task][i-1] == var:
									del ans[task][i-1] #пересмотреть
				ans[task] = ' '.join(ans[task])
				if ans[task] == j_task:
					ans[task] = ans[task].replace('спасибо', '').replace('  ', ' ').strip()
					ans.insert(task, 'спасибо')

		if 'сара' in ans:
			if len(ans) > 1:
				del ans[ans.index('сара')]
		n_ans = []

		for i in range(len(ans)):
			if (ans[i].startswith('привет') or ans[i].endswith('привет')):
				if ans[i].startswith('привет'):
					n_ans.append('привет')
					if ans[i].replace('привет', '').strip() != '':
						n_ans.append(ans[i].replace('привет', '').strip())
				if ans[i].endswith('привет'):
					if ans[i].replace('привет', '').strip() != '':
						n_ans.append(ans[i].replace('привет', '').strip())
					n_ans.append('привет')
			else:
				if ans[i]:
					n_ans.append(ans[i])

		n_ans = self.delete_doubles2(n_ans)

		ans = []
		last = ''
		for task in n_ans:
			if task != last:
				ans.append(task)
				last = task

		tasklist = self.delete_doubles2([value for value in ans if value])

		ultimate_task = []

		def check_weather(task):
			mas = ('подскажи', 'скажи')
			s_task = task.split()
			if s_task[0] in (mas):
				if s_task[1] in ['какая', 'что', 'как']:
					if ('погода' in task) or ('температура' in task):
						self.weather()
					else:
						self.web_talk(task)
				else:
					self.web_talk(task)

		nones = choice(['Давайте вы как-нибудь сами найдете то, что вам надо', 'Лучше вас никто не найдет', 'Мне лень'])


		#print(self.phrases)
		#input(tasklist)

		for task in tasklist:
			if task:
				first_word = task.split()[0]
				for vat in ['можешь', 'давай']:
					if rat(first_word, val) > 70:
						if val in task.split():
							if not(rat(task.split()[task.split().index(val) + 1], 'поработаем') > 70):
								task = task.replace(first_word, '', 1).strip()
								if task:
									first_word = task.split()[0]
								else:
									first_word = ''
				if first_word:

					if self.comparison(first_word, ['где']):
						self.search_on_map(task.replace(first_word, '').strip())

					elif self.comparison(first_word, ['поищи']) or (first_word in ['найди', 'найти']):
						if self.not_answers == False:
							n_task = task.split()
							flag = 0
							for val in ['где', 'ближайший', 'поблизости']:
								if rat(n_task[1], val) > 70:
									flag = 1
									break
							if flag:
								self.search_on_map(task.replace(first_word, '').strip())
							else:
								self.web_search(task)
						else:
							self.add_phrases(nones)

					elif check_weather(task):
						if self.not_answers == False:
							self.weather()
						else:
							self.add_phrases(nones)

					elif self.comparison(first_word, ['расскажи', 'объясни', 'подскажи', 'скажи']):
						if self.not_answers == False:
							self.web_talk(task)
						else:
							self.add_phrases(nones)

					elif ('новости' in task) and not(self.comparison(' '.join(task.split()[0:2]), ['что такое', 'как понять'])):
						self.show_news(task)

					elif (task.startswith('напомни') or task.startswith('напомнишь')):
						self.create_remind(f"{task.replace('напомни', '').replace('напомнишь', '')}")

					elif (self.comparison(first_word, ['создай'])) or (self.comparison(' '.join(task.split()[0:2]), ['давай поработаем'])):
						self.create_new_project(task)

					elif task.startswith(('зайди на', 'заходи на', 'перейди на', 'зайди в', 'заходи в', 'перейди в')):
						for i in ('зайди на', 'заходи на', 'перейди на', 'зайди в', 'заходи в', 'перейди в'):
							task = task.replace(i, '').replace(' ','').strip()
						self.go_to_page(task)

					else:
						if rat(task.split()[0], 'открой') > 80:
							if ' '.join(task.split()[1:]) in ('расписание', 'сайт кнагу', 'сайт канаву', 'adsense', 'мой канал', 'канал', 'гитхаб', 'гит', 'репост'):
								self.go_to_page(task)

						elif task.split()[0] in ['расскажи', 'объясни', 'подскажи', 'скажи']:
							task = task.split()
							del task[0]
							task = ' '.join(task)

						elif self.check_get_ideas(task):
							self.get_ideas(task)


						elif self.comparison(task.split()[0], ['чем', 'кто', 'что', 'какой', 'который', 'где', 'когда', 'почему', 'зачем', 'куда', 'откуда', 'кого', 'какого', 'чей', 'сколько', 'как', 'кому', 'кем']):



							if task.split()[0] == 'что':
								if ('сегодня' in task) or ('нового' in task):
									self.show_news(task)
								elif self.comparison(task, ['что делаешь', 'чем занимаешься']):
									self.what_doing()
								else:
									self.web_search(f'найди {task}')
									self.web_talk(f'найди {task}')
							elif not(self.search_exe_function(task)):
								self.web_search(f'найди {task}')
								self.web_talk(f'найди {task}')
						recognized_task = self.search_exe_function(task)

						if recognized_task:
							ultimate_task.append(recognized_task)

		ultimate_tasks = self.delete_doubles2(ultimate_task)
		for var in self.one_time_executable:
			if ultimate_task.count(var) > 1:

				ultimate_tasks = ultimate_tasks[::-1]

				for i in range(ultimate_tasks.count(var) - 1):
					del ultimate_tasks[ultimate_task.index(var)]

				ultimate_tasks = ultimate_task[::-1]

		return ultimate_tasks