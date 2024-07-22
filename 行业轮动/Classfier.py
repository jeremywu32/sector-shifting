import numpy as np
import pandas as pd

class Classfier:
    def __init__(self):
        print()

    def classify_macro(self, macro_indicator):
        if macro_indicator >= 0:
            return 1
        else:
            return -1

    def classify_styles(self, factor_stats: dict):
        styles = []
        for key in factor_stats.keys():
            median = factor_stats[key][0]
            prob = factor_stats[key][1]
            if median >= 53 and prob >= 0.8:
                styles.append(1)
            elif median <= 47 and prob <= 0.2:
                styles.append(-1)
            else:
                styles.append(0)
        return styles