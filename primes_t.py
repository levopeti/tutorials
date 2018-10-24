import sys
import numpy as np
import math

primes = np.array([2])                          # sys.maxsize = 9.223.372.036.854.775.807
len_primes = np.array([0])
for n in range(3, sys.maxsize, 2):

    cut_primes = primes[primes <= math.floor(math.sqrt(n))]
    # filtered_primes = list(filter(lambda x: (n % x == 0), cut_primes))
    #
    # if len(filtered_primes) == 0:
    #     primes = np.append(primes, n)

    for prime in cut_primes:
        if n % prime == 0:
            break
    else:
        primes = np.append(primes, n)

    if (n + 1) % 100000 == 0:
        len_primes = np.append(len_primes, len(primes))
        print('Length of primes list: {}'.format(len_primes[-1]))
        print('Number of new primes: {}'.format(len_primes[-1] - len_primes[-2]))
        print('n: {:.3e}'.format(n + 1))
        print()

print(primes[-1])





# import numpy as np
# import math
#
# max_number = int(input())                       # max number of serching
# primes = np.array([2])                          # sys.maxsize = 9.223.372.036.854.775.807
# len_primes = np.array([0])
# for n in range(3, max_number, 2):
#
#     cut_primes = primes[primes <= math.floor(math.sqrt(n))]
#
#     for prime in cut_primes:
#         if n % prime == 0:
#             break
#     else:
#         primes = np.append(primes, n)
#
#     if (n + 1) % 100000 == 0:
#         len_primes = np.append(len_primes, len(primes))
#
# print('The largest prime number: {}'.format(primes[-1]))

