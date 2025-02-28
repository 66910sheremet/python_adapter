from backtrader.dataseries import TimeFrame
from moexalgo_fork import session_moexalgo_proxy, Market

from .moexalgo_feed_moexISS import AlgoDataMoexISS


class MoexAlgoStore(object):
    """Класс получения данных по тикеру"""
    _GRANULARITIES = {  # Все временнЫе интервалы
        (TimeFrame.Minutes, 1): '1min',
        (TimeFrame.Minutes, 5): '5min',  # need to be resampled from 1m
        (TimeFrame.Minutes, 10): '10min',
        (TimeFrame.Minutes, 30): '30min',  # need to be resampled from 10m
        (TimeFrame.Minutes, 60): '1h',
        (TimeFrame.Days, 1): '1d',
        (TimeFrame.Weeks, 1): '1w',
        (TimeFrame.Months, 1): '1m',
    }

    def __init__(self, login="", password=""):
        """Инициализация необходимых переменных"""
        self.market = Market('stocks')
        self._cash = 0
        self._value = 0
        self._data = None
        self._datas = {}

        if login and password:
            session_moexalgo_proxy.authorize(login, password)  # Авторизуемся на Московской Бирже
            print("Авторизуемся на Московской Бирже")

    def getdata(self, **kwargs):  # timeframe, compression, from_date=None, live_bars=True
        """Метод получения исторических и live данных по тикеру"""
        symbol = kwargs['dataname']
        compression = 1
        metric = ''
        if 'compression' in kwargs: compression = kwargs['compression']
        if 'metric' in kwargs: metric = kwargs['metric']
        # print('metric', metric)
        tf = self.get_interval(kwargs['timeframe'], compression)

        if symbol not in self._datas:
            self._datas[f"{symbol}{tf}{metric}"] = AlgoDataMoexISS(store=self, **kwargs)  # timeframe=timeframe, compression=compression, from_date=from_date, live_bars=live_bars
        return self._datas[f"{symbol}{tf}{metric}"]

    def get_interval(self, timeframe, compression):
        """Метод получения ТФ по тикеру для moexalgo_fork из ТФ backtrader"""
        return self._GRANULARITIES.get((timeframe, compression))

    def get_symbol_info(self, symbol):
        """Метод получения информации по тикеру"""
        return self.market._ticker_info(symbol)
