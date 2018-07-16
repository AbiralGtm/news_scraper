from Rashifal.prediction import RashifalPrediction
from Rashifal.yearly import YearlyRashifal
from forex.forex import ForeignExchangeRate


# forex, yearly_rashifal, rashifal_prediction


def run_forex_n_rashifal():
    fe = ForeignExchangeRate()
    fe.put_to_database()
    yr = YearlyRashifal()
    yr.put_to_database()
    pred = RashifalPrediction()
    pred.put_to_database()


if __name__ == '__main__':
    run_forex_n_rashifal()



