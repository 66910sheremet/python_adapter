from pykson import Pykson, JsonObject, StringField, DateTimeField, FloatField


class CandleDto(JsonObject):
    open = FloatField()
    close = FloatField()
    high = FloatField()
    low = FloatField()
    value = FloatField()
    volume = FloatField()
    begin = DateTimeField(datetime_format='%Y-%m-%dT%H:%M:%S')
    end = DateTimeField(datetime_format='%Y-%m-%dT%H:%M:%S')

    def to_dict(self):
        return {
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'value': self.value,
            'volume': self.volume,
            'begin': self.begin,
            'end': self.end
        }
