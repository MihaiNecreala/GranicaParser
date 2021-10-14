import itertools
import re

from combinator import add_r_space

VSE = (
    'вся ', 'все ', 'всё ', 'весь ',
)
PREFIX = (
    'ноль', 'нейтральной полосе', 'нейтральная полоса', 'под навесом', 'навесе', 'навес', 'нейтралка',
    'нейтральная', 'нейтральной', 'нетралка', 'нитралка', 'нейтралке', 'нетралке', 'буфер', 'буфере',
    'нейтраль', 'нейтрале', 'нейтрали', 'серая', 'серая зона', 'буферная зона', 'серой', 'серой зоне', 'буферной зоне',
    'промзона', 'промзоне', 'нулевик', 'нулевой', 'терминале', 'терминал'
)
MIDDLE = (
    'битком', 'забито', 'забита', 'забитый', 'полно', 'полный', 'полная', 'пустой', 'пустая', 'пусто', 'забит',
    'битком', 'есть', 'никого',
)
AUX = (
    'один ряд', 'два ряда', '1 ряд', '2 ряда', '2 рчда', '3 ряда', '4 ряда', 'две границы', 'обе границы',
    'навес и ноль', 'две таможни', 'две полосы', 'три полосы', 'одна полоса', 'движение ноль', 'движения ноль',
    'был пустой', 'было пусто', 'движение 0', 'движения 0', 'две очереди', 'три очереди', 'одна очередь',
    'много фур',
)
DIGITS = (
    'одна', 'одну', 'две', 'пару', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'сем', 'восемь', 'восем',
    'девять', 'десять',
)
TIME = (
    'часа', 'часа на', 'часов', 'час', 'минуты', 'минут', 'мин', 'ч', 'утра', 'вечера',
)
TRUCKS = (
    'грузовая', 'грузовых', 'фура', 'фуры', 'фур',
)
KM = (
    'км', 'километр',
)
PRODVIN = (
    'продвинулись', 'продвинулось', 'продвинулась',
)


class Cleaner:
    combinations = ()

    def __init__(self):
        combs = [''.join(s) for s in itertools.product(add_r_space(PREFIX), MIDDLE)]
        combs_vse = [''.join(s) for s in itertools.product(add_r_space(PREFIX), VSE, MIDDLE)]
        combs_dt = [''.join(s) for s in itertools.product(add_r_space(DIGITS), TIME)]
        combs_km = [''.join(s) for s in itertools.product(add_r_space(DIGITS), KM)]
        combs_mest = [''.join(s) for s in itertools.product(add_r_space(DIGITS), 'мест')]
        combs_td = [''.join(s) for s in itertools.product(add_r_space(TIME), DIGITS)]
        combs_prodv = [''.join(s) for s in itertools.product(add_r_space(PRODVIN), DIGITS)]
        combs_prodv_na = [''.join(s) for s in itertools.product(add_r_space(PRODVIN), add_r_space(('на',)), DIGITS)]
        combs_gruz = [''.join(s) for s in itertools.product(add_r_space(DIGITS), TRUCKS)]

        self.combinations = tuple(combs + combs_vse + combs_td + combs_dt + combs_gruz + combs_km + combs_prodv +
                                  combs_prodv_na + combs_mest) + AUX

    @staticmethod
    def clear_prodvin(msg):
        prodv = '|'.join((tuple([''.join(s) for s in itertools.product(add_r_space(PRODVIN), ('на', 'в'))]) + PRODVIN))
        ret = re.sub(fr'(?:{prodv}) \d+', '', msg).replace('  ', ' ')
        return ret

    @staticmethod
    def clear_other(msg):
        km = '|'.join(KM)
        ret = re.sub(fr'\d+ (?:{km})', '', msg).replace('  ', ' ')
        ret = re.sub(fr'\d+ мест', '', ret).replace('  ', ' ')
        return ret

    @staticmethod
    def clear_trucks(msg):
        trucks = '|'.join(TRUCKS)
        ret = re.sub(fr'\d+ (?:{trucks})', '', msg).replace('  ', ' ')
        return ret

    @staticmethod
    def clear_times(msg):
        times = '|'.join(TIME)
        msg = re.sub(fr'\d+ (?:{times})', '', msg).replace('  ', ' ')
        ret = re.sub(fr'(?:{times}) \d+', '', msg).replace('  ', ' ')
        return ret

    @staticmethod
    def clear_rational_number(msg):
        ret = re.sub(r'\d+[,.]\d+', '', msg).replace('  ', ' ')
        return ret

    def clean(self, msg):
        all_combs = '|'.join(self.combinations)
        res = re.findall(fr'\d+ (?:{all_combs}) \d+', msg)
        if len(res):  # только если нашлись комбинации \d+ фраза \d+
            print('Clean exception finded')
            return msg

        # msg = self.clear_trucks(msg)
        msg = self.clear_prodvin(msg)
        msg = self.clear_times(msg)
        msg = self.clear_other(msg)

        for item in self.combinations:
            i = msg.find(item)
            if i != -1:
                msg = msg.replace(item, '')

        return msg
