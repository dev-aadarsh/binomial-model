import numpy as np
import pandas as pd
from scipy.special import comb

def build_price_df(init_price, up_mul, down_mul, num_iterations):
    price_df = pd.DataFrame(np.zeros((num_iterations + 1, num_iterations + 1)))
    price_df.loc[0][0] = init_price

    for time_idx in range(1, num_iterations + 1):
        for state_idx in range(time_idx + 1):
            price_df.iloc[state_idx, time_idx] = price_df.iloc[state_idx, time_idx - 1] * up_mul

        # A new state has to be added in each iteration
        price_df.iloc[time_idx, time_idx] = price_df.iloc[time_idx - 1, time_idx - 1] * down_mul

    return price_df

def build_prob_df(num_iterations, q_u, q_d):
    prob_df = pd.DataFrame(np.zeros((num_iterations + 1, num_iterations + 1)))
    prob_df.loc[0][0] = 1

    for time_idx in range(1, num_iterations + 1):
        for state_idx in range(time_idx + 1):
            val = comb(time_idx, state_idx) * q_d**state_idx * q_u**(time_idx-state_idx)
            prob_df.iloc[state_idx, time_idx] = val

    return prob_df

def calc_period_length(time_years, num_iterations):
    h = time_years / num_iterations
    return h

def calc_multipliers(sigma, period_length):
    up_mul = np.exp(sigma * np.sqrt(period_length))
    down_mul = np.exp(-sigma * np.sqrt(period_length))
    return up_mul, down_mul

def calc_prob(up_mul, down_mul, rf, period_length):
    q_u = (np.exp(rf * period_length) - down_mul)/(up_mul - down_mul)
    q_d = 1 - q_u
    return q_u, q_d

def calc_eu_call_price(init_price, time_years, num_iterations, sigma, rf, strike_price):
    period_length = calc_period_length(time_years, num_iterations)
    up_mul, down_mul = calc_multipliers(sigma, period_length)

    price_df = build_price_df(init_price, up_mul, down_mul, num_iterations)
    price_df

    q_u, q_d = calc_prob(up_mul, down_mul, rf, period_length)

    prob_df = build_prob_df(num_iterations, q_u, q_d)
    prob_df

    expected_stock_price = np.dot(price_df[5], prob_df[5])
    expected_call_payoff = expected_stock_price - strike_price
    discount_factor = np.exp(-rf * time_years)

    call_price = expected_call_payoff * discount_factor
    return call_price