class DepthValueGetter:
    def get(self, text):
        if (text == 'Минимальная'):
            depth = 30
        if (text == 'Средняя'):
            depth = 60
        if (text == 'Максимальная'):
            depth = 90
        return depth