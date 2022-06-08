class language():
    def __init__(self):
        self.lang = 'en'

        self.json = None

        self.set_lang(self.lang)

    def set_lang(self, lang):
        try:
            self.json = read_dict('assets/lang/' + lang)
            self.lang = lang

            return True

        except Exception as e:
            print('set_lang: ', e)
            return False

language = language()
