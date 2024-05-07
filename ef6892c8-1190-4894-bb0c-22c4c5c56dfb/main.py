from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import ATR, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Choosing SPY as it has a very liquid options market
        return ["SPY"]

    @property
    def interval(self):
        # Daily data to assess the broader movement trends
        return "1day"

    def run(self, data):
        # Ideally, we would look for conditions such as low volatility,
        # but here we will use ATR as a proxy for market movement assessment.
        spy_atr = ATR("SPY", data["ohlcv"], 14)  # 14-day Average True Range
        spy_sma = SMA("SPY", data["ohlcv"], 20)  # 20-day Simple Moving Average

        if len(spy_atr) == 0 or len(spy_sma) == 0:
            return TargetAllocation({})

        # Basic logic for demonstration:
        # If the current ATR is low compared to its recent historical range,
        # this may indicate low volatility, a condition under which iron condors perform well.
        atr_low = spy_atr[-1] < min(spy_atr[-14:])
        # Ensure the price is around the SMA, indicating sideway movement.
        price_near_sma = abs(data["ohlcv"][-1]["SPY"]["close"] - spy_sma[-1]) <= (spy_sma[-1] * 0.02)

        if atr_low and price_near_sma:
            log("Iron condor potential setup found")
            # This doesn't execute the iron condor but signals potential setup.
            # Allocation remains 0 as this strategy is for demonstration.
            return TargetAllocation({})
        else:
            log("No iron condor setup")
            return TargetAllocation({})