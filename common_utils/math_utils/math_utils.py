import math

def gaussian(x, mu, sigma):
    coeff = 1/(2*math.pi*sigma**2)**0.5
    power = (-(x - mu)**2)/(2*sigma**2)
    return coeff * math.exp(power)