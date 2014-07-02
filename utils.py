from distutils.util import strtobool

def yes_or_no(question):
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please answer by \'y\' or \'n\'.\n')
		except KeyboardInterrupt:
			return False
			
