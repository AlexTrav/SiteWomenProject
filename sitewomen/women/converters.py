class FourDigitYearConverter:
    regex = '[0-9]{4}'

    @staticmethod
    def to_python(value):
        return int(value)

    @staticmethod
    def to_url(value):
        return '%04d' % value
    