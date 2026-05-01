import re

from rest_framework.serializers import ValidationError


class YoutubeChanelValidator:
    """ Класс проверяет отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""

    def __init__(self, field):
        """Инициализирует поле для проверки"""
        self.field = field

    def __call__(self, value):
        """ Допускает ссылки ведущие только на youtube.com"""
        if value.get(self.field):
            regexp_youtube = re.compile(r'^(https?://)?(www\.)?(youtube\.com)/.+')
            tmp_val = dict(value).get(self.field)
            if not bool(regexp_youtube.match(tmp_val)):
                raise ValidationError("Допускаются ссылки ведущие только на youtube.com")
