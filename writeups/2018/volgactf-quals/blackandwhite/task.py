#!/usr/bin/env python
from __future__ import division
import numpy as np
import scipy.misc as scmisc


T1 = 64
T2 = 192
C = scmisc.imread('lena.tif')
CB = scmisc.imread('lena_bin.tif', mode='L') // 255
W = scmisc.imread('flag.tif', mode='L') // 255
u = np.zeros((514, 514))
CW = np.zeros((514, 514))
u[1:513, 1:513] = C
for n1 in range(1, 513):
    for n2 in range(1, 513):
        if (u[n1,n2]>=T1 and (W[n1-1,n2-1] ^ CB[n1-1,n2-1]==1)) or (u[n1,n2]>=T2 and (W[n1-1,n2-1] ^ CB[n1-1,n2-1]==0)):
            CW[n1, n2] = 1
        elif (u[n1,n2]<T1 and (W[n1-1,n2-1] ^ CB[n1-1,n2-1]==1)) or (u[n1,n2]<T2 and (W[n1-1,n2-1] ^ CB[n1-1,n2-1]==0)):
            CW[n1, n2] = 0
        e = 255*CW[n1,n2] - u[n1,n2]
        u[n1, n2+1] = u[n1, n2+1] - e*(7/16)
        u[n1+1, n2-1] = u[n1+1, n2-1] - e*(3/16)
        u[n1+1, n2] = u[n1+1, n2] - e*(5/16)
        u[n1+1, n2+1] = u[n1+1, n2+1] - e*(1/16)
CW = np.array(CW[1:513, 1:513], dtype=int)
scmisc.imsave('embed.tif', 255*CW)
flag_image = 255*np.bitwise_xor(CW, CB)
