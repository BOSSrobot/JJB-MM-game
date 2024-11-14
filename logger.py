class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.f = None

    def log(self, message):
        if self.f is None:
            self.f = open(self.log_file, 'a')
        self.f.write(message + '\n')

    def error(self, message):
        self.log(f'[ERROR]:   {message}')

    def warning(self, message):
        self.log(f'[WARNING]: {message}')

    def info(self, message):
        self.log(f'[INFO]:    {message}')

    def spacing(self):
        self.log('')
        self.log('------------------------------------------------------------')
        self.log('')

# [LOG]:     |
# [ERROR]:   |
# [WARNING]: |