#!/usr/bin/env python3

# Date:     2025-05-23
# Author:   Tamas Vince
# Purpose:  Pretty self-explanatory
# Runtime:  N/A

# WARN: This looks awful in plaintext,
# please review thinking.md for LaTeX formatted version


# 1.
# please refer to thinking.md for
# the explanation
print('1.: 5')

# 2.
print('2.:')

# 3.
print('3.:')

# 4.
# (n^2)^n  - 2n^n + 1 = 0
# ha n < 0 es a kifejezes ertelmezett, akkor
# (n^2)^n > 0 es -2n^n > 0 vagyis
# (n^2)^n - 2n^n + 1 > 0 nincs megoldasa
# igy csak n > 0 eseten keresunk megoldast
# n > 0 eseten:
# (n^2)^n = (n^n)^2 vagyis
# (n^n)^2 - 2n^2 + 1 = 0
# vezessuk le: n^n = x
# x^2 - 2x + 1 = 0
# (x-1)^2 = 0
# x = 1
# n^n = 1
# n = 1
print('4.: 1')

# 5.
# Ha a ket abrat egymasra tesszuk az
# pont ket asztal + 1 teknos + 1 cica
# T = teknos
# C = cica
# A = asztal
# 130 + C + 170 + T = 2A + M = T
# 300 + M + T = 2A + M + T
# 300 = 2A
# A = 150
print('5.: 150')

# 6.
# C = cica
# K = kutya
# P = patkany
# 10 + 20 + 24 = 2C + 2K + 2P
# 54 = 2 * (M + K + P)
# M + K + P = 27
print('6.: 27')

# 7.
# esely hogy egyikuk se dob hatost elsore: (5/6)^2
# ha nem nyert senki az elso korben akkor a jatek resetel,
# tehat az esely ugyanaz mint 3 sorral ezelott
# tehat esely = 1/6+25/36*p = 6/11
print('7.: 6/11')
