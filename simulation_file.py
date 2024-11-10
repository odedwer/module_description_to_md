import numpy as np
import scipy
import scipy.stats as stats
import matplotlib.pyplot as plt

PARAM1 = 0.5
PARAM2 = 50
PARAM3 = 75
PARAM4_TEST = 100


def some_function():
    """
    This function calculates the product of PARAM1 and PARAM2.
    """
    return PARAM1 * PARAM2


def another_function(var1, var2):
    """
    This function calculates the sum of two variables and divides it by PARAM3.
    :param var1: The first number
    :param var2: The second number
    """
    return (var1 + var2) / PARAM3


def main():
    print(some_function())
    print(another_function(10, 20))

    x = np.linspace(0, 100, 1000)
    y = stats.norm.pdf(x, PARAM4_TEST, 10)
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
