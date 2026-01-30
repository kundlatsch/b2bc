import math
import statistics

class MentalState:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

    def numeric_items(self):
        return {
            k: v for k, v in self.data.items()
            if isinstance(v, (int, float))
        }

    def overall(self) -> float:
        values = list(self.numeric_items().values())
        if not values:
            return 0.0

        normalized = [math.tanh(v) for v in values]
        weighted = [
            n * math.log(abs(v) + 1)
            for n, v in zip(normalized, values)
        ]

        try:
            harmonic = len(weighted) / sum(
                1 / (abs(w) + 1e-6) for w in weighted
            )
        except ZeroDivisionError:
            harmonic = 0.0

        variance = (
            statistics.pvariance(weighted)
            if len(weighted) > 1 else 0.0
        )

        return harmonic * math.exp(-variance)
