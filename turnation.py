import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
import modello_turnazione as Model
import itertools
import sys
import os

params = pd.read_csv(sys.argv[1], sep=';', names=['param', 'value'],
                     nrows=6, usecols=[0, 1])

OPERATORS, DAYS, TIMESLOTS, WORKSHIFTS, WORKINGHOURS, THETA = params.value

S_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6, nrows=TIMESLOTS)
AV_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 1, nrows=OPERATORS)
B_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + OPERATORS + 2, nrows=OPERATORS)
O_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 2 * OPERATORS + 3, nrows=OPERATORS)
N_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 3 * OPERATORS + 4, nrows=OPERATORS)
V_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 4 * OPERATORS + 5, nrows=OPERATORS)
FH_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 5 * OPERATORS + 6, nrows=OPERATORS)
FS_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 6 * OPERATORS + 7, nrows=OPERATORS)
PS_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 7 * OPERATORS + 8, nrows=OPERATORS)
PR_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 8 * OPERATORS + 9, nrows=OPERATORS)
L_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 9 * OPERATORS + 10, nrows=OPERATORS)
_1C_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 10 * OPERATORS + 11, nrows=OPERATORS)
_1A_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 11 * OPERATORS + 12, nrows=OPERATORS)
_2A_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 12 * OPERATORS + 13, nrows=OPERATORS)
_1B_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 13 * OPERATORS + 14, nrows=OPERATORS)
H_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 14 * OPERATORS + 15, nrows=1)
SO_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 14 * OPERATORS + 17, nrows=1)
W_ = pd.read_csv(sys.argv[1], sep=';', skiprows=6 + TIMESLOTS + 14 * OPERATORS + 19, nrows=1)
# ABS_ = pd.read_csv("turnazione.csv", sep=';', skiprows=5 + TIMESLOTS + 9 * OPERATORS + 10, nrows=OPERATORS)

S = {}
AV = {}
B = {}
O = {}
N = {}
V = {}
F = {}
Z = {}
PS = {}
PR = {}
L = {}
_1C = {}
_1A = {}
_2A = {}
_1B = {}
H = {}
W = {}
Q = {}
I = {}
C = {}
OH = {}
MH = {}
SO = {}
coefficients = {}
# ABS = {}

for i in range(TIMESLOTS):
    for j in range(DAYS):
        S[i + 1, j + 1] = S_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        AV[i + 1, j + 1] = AV_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        B[i + 1, j + 1] = B_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        O[i + 1, j + 1] = O_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        N[i + 1, j + 1] = N_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        V[i + 1, j + 1] = V_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        PS[i + 1, j + 1] = PS_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        PR[i + 1, j + 1] = PR_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        L[i + 1, j + 1] = L_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        _1C[i + 1, j + 1] = _1C_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        _1A[i + 1, j + 1] = _1A_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        _2A[i + 1, j + 1] = _2A_.values[i, j]

for i in range(OPERATORS):
    for j in range(DAYS):
        _1B[i + 1, j + 1] = _1B_.values[i, j]

for i in range(WORKSHIFTS):
    H[i + 1] = H_.values[0, i]

for i in range(TIMESLOTS):
    W[i + 1] = W_.values[0, i]

for i in range(OPERATORS):
    SO[i + 1] = SO_.values[0, i]

for i in range(OPERATORS):
    for j in range(DAYS):
        Q[i + 1, j + 1] = FH_.values[i, j]

for i in range(OPERATORS):
    if (i + 1) not in I:
        I[i + 1] = set()
    for j in range(DAYS):
        if FH_.values[i, j] == 1:
            I[i + 1].add(j + 1)

for i in range(OPERATORS):
    if (i + 1) not in C:
        C[i + 1] = set()
    for j in range(DAYS):
        if FS_.values[i, j] == 1:
            C[i + 1].add(j + 1)

for i in range(OPERATORS):
    for j in range(DAYS):
        if (j + 1) not in I[i + 1]:
            if C[i + 1]:
                prod = 1
                for d in C[i + 1]:
                    prod *= abs((j + 1) - d)
                coefficients[i + 1, j + 1] = prod
            else:
                coefficients[i + 1, j + 1] = sys.maxsize
        else:
            coefficients[i + 1, j + 1] = 0

for i in range(OPERATORS):
    OH[i + 1] = len(C[i + 1])

for i in range(OPERATORS):
    MH[i + 1] = len(I[i + 1])

# for i in range(OPERATORS):
#     for j in range(DAYS):
#         ABS[i + 1, j + 1] = ABS_.values[i, j]

dataDict = {None: {
      'p': {None: OPERATORS},
      'd': {None: DAYS},
      'f': {None: TIMESLOTS},
      't': {None: WORKSHIFTS},
      'wh':{None: WORKINGHOURS},
      'th': {None: THETA},
      'S': S,
      'AV': AV,
      'B': B,
      'O': O,
      'N': N,
      'V': V,
      'U': _1B,
      'Z': PS,
      'J': PR,
      'L': L,
      'E': _1A,
      'R': _2A,
      'G': _1C,
      'H': H,
      'W': W,
      'Q': Q,
      'OH': OH,
      'MH': MH,
      'SO': SO,
      'COEFF': coefficients
}}

outfile = os.getcwd() + '/out/ciccio'
solverfile = 'C:\\Users\Alberto\PycharmProjects\TOP\prova\log.log'

res, time = Model.minimize(dataDict, outfile, solverfile)