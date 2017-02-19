import markovify

def gen_filename():
		counter = 0
		while True:
			yield 'markov{}.txt'.format(counter)
			counter += 1

file_iter = gen_filename()


def create_text(text, len = 100000):
	filename = next(file_iter)
	text_model = markovify.Text(text)
	f = open(filename, 'w+')
	for i in range(len):
		f.write(text_model.make_sentence())
	f.close()

