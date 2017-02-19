import markovify

def gen_filename():
		counter = 0
		while True:
			yield 'markov{}.txt'.format(counter)
			counter += 1

def get_text(loc):
    with open(loc) as f:
        text = f.read()
    return text.replace('\n', '')

file_iter = gen_filename()

def create_text(url, len = 100000):
	filename = next(file_iter)
	text_model = markovify.Text(get_text(url))
	f = open(filename, 'w+')
	for i in range(len):
		try:
			print('progress: {}'.format(i))
			f.write(text_model.make_sentence())
		except TypeError:
			continue
	f.close()
