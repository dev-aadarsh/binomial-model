import numpy as np
import pandas as pd

def build_price_df(init_price, up_mul, down_mul, num_iterations):
    price_df = pd.DataFrame(np.zeros((num_iterations, num_iterations)))
    price_df.loc[0][0] = init_price

    for time_idx in range(1, num_iterations):
        for state_idx in range(time_idx + 1):
            price_df.iloc[state_idx, time_idx] = price_df.iloc[state_idx, time_idx - 1] * up_mul

        # A new state has to be added in each iteration
        price_df.iloc[time_idx, time_idx] = price_df.iloc[time_idx - 1, time_idx - 1] * down_mul

    return price_df