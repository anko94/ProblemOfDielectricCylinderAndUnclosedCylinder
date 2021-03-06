import math
import mpmath
import numpy as np
from multiprocessing import Pool
from functools import partial
import time
import cmath


def AMP(i, n, nDielectric, G, P, c1, c2, ds, dl, k0):
    A = []
    for j in range(n):
        i1 = 1 if i == j and j < nDielectric and i < nDielectric else 0
        if j < nDielectric:
            A.append(complex(c1 * ds * (G(k0, P[i], P[j]) - 1 / (c1 * ds) * i1)))
        else:
            A.append(complex(c2 * dl * G(k0, P[i], P[j])))
    return A


class Solver:

    def getInitialFieldStrength(self, k, P, P0):
        r = math.sqrt((P0[0] - P[0]) ** 2 + (P0[1] - P[1]) ** 2)
        r = r if r != 0 else self.accuracy
        return mpmath.hankel1(0, k * r)

    def G(self, k, M, P):
        r = math.sqrt((M[0] - P[0])**2 + (M[1] - P[1])**2)
        r = r if r != 0 else self.accuracy
        return math.pi/2 * 1j * mpmath.hankel1(0, k * r)

    def hankelInfinity(self, k, M, P):
        r = math.sqrt((M[0] - P[0]) ** 2 + (M[1] - P[1]) ** 2)
        return math.sqrt(2/(math.pi*k*r)) * cmath.exp(1j*(k*r-math.pi/4))

    def Ginfinity(self, k, M, P):
        return math.pi / 2 * 1j * self.hankelInfinity(k, M, P)

    def solve(self, nDielectric, nArc, dielectricRectangles, arcPoints, source):
        vertices = dielectricRectangles[0].getListOfVertices()
        self.ds = math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2) * \
             math.sqrt((vertices[1][0] - vertices[3][0])**2 + (vertices[1][1] - vertices[3][1])**2)
        self.dl = math.sqrt((arcPoints[0][0]-arcPoints[1][0])**2 + (arcPoints[0][1]-arcPoints[1][1])**2)
        print("ds: ", self.ds)
        print("dl: ", self.dl)
        B = []
        self.P = []
        startTime = time.time()
        for i in range(nDielectric):
            vertices = dielectricRectangles[i].getListOfVertices()
            self.P.append([vertices[1][0] - math.fabs(vertices[1][0] - vertices[2][0]) / 2,
                 vertices[1][1] - math.fabs(vertices[1][1] - vertices[2][1]) / 2])
            B.append(-complex(self.getInitialFieldStrength(self.k0, self.P[i], source.point)))
        for i in range(nArc):
            self.P.append([arcPoints[i][0], arcPoints[i][1]])
            B.append(-complex(self.getInitialFieldStrength(self.k0, self.P[i+nDielectric], source.point)))
        A = [[complex(0.0)] * (nDielectric+nArc) for i in range(nDielectric+nArc)]
        n = nDielectric+nArc
        pool = Pool(16)
        A = pool.map(partial(AMP, n=n, nDielectric=nDielectric, G=self.G,
                         P=self.P, c1=self.c1, c2=self.c2, ds=self.ds, dl=self.dl, k0=self.k0), list(range(n)))
        # for i in range(n):
        #     for j in range(n):
        #         i1 = 1 if i==j and j<nDielectric and i<nDielectric else 0
        #         if j<nDielectric:
        #             A[i][j] = complex(self.c1*self.ds*(self.G(self.k0, self.P[i], self.P[j])-1/(self.c1*self.ds)*i1))
        #         else:
        #             A[i][j] = complex(self.c2*self.dl*self.G(self.k0, self.P[i], self.P[j]))
        endTime = time.time()
        print(endTime-startTime)
        result = np.linalg.solve(np.array(A), np.array(B))
        endTime1=time.time()
        print(endTime1-endTime)
        U = result[:nDielectric]
        PHI = result[nDielectric:]
        return [U, PHI]

    def getFieldEInPointM(self, UPHI, M, source, nDielectric):
        U = UPHI[0]
        PHI = UPHI[1]
        Ez = complex(self.getInitialFieldStrength(self.k0, M, source.point))
        Hx = complex(1 / math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2) *
                     (M[1] - source.point[1]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
            (M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2))))
        Hy = complex(1 / math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2) *
                     (M[0] - source.point[0]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
            (M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2))))
        for i in range(len(U)):
            Ez += complex(self.c1 * U[i] * self.G(self.k0, M, self.P[i]) * self.ds)
            Hx += complex(self.c1 * U[i] * self.ds * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2) *
                          (M[1] - self.P[i][1]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
            Hy += complex(self.c1 * U[i] * self.ds * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2) *
                          (M[0] - self.P[i][0]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
        for i in range(len(PHI)):
            Ez += complex(self.c2 * PHI[i] * self.G(self.k0, M, self.P[i + nDielectric]) * self.dl)
            Hx += complex(self.c2 * PHI[i] * self.dl * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2) *
                          (M[1] - self.P[i + nDielectric][1]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2))))
            Hy += complex(self.c2 * PHI[i] * self.dl * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2) *
                          (M[0] - self.P[i + nDielectric][0]) * (-mpmath.hankel1(1, self.k0 * math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2))))
        Hx *= - complex(0, 1)
        Hy *= complex(0, 1)
        return [Ez, Hx, Hy]

    def getFieldEInPointMInfinity(self, UPHI, M, nDielectric):
        U = UPHI[0]
        PHI = UPHI[1]
        Ez = complex(0)
        Hx = complex(0)
        Hy = complex(0)
        for i in range(len(U)):
            Ez += complex(self.c1 * U[i] * self.Ginfinity(self.k0, M, self.P[i]) * self.ds)
            Hx += complex(self.c1 * U[i] * self.ds * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2) *
                          (M[1] - self.P[i][1]) * (-self.hankelInfinity(self.k0, M, self.P[i])))
            Hy += complex(self.c1 * U[i] * self.ds * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2) *
                          (M[0] - self.P[i][0]) * (-self.hankelInfinity(self.k0, M, self.P[i])))
        for i in range(len(PHI)):
            Ez += complex(self.c2 * PHI[i] * self.Ginfinity(self.k0, M, self.P[i + nDielectric]) * self.dl)
            Hx += complex(self.c2 * PHI[i] * self.dl * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2) *
                          (M[1] - self.P[i + nDielectric][1]) * (-self.hankelInfinity(self.k0, M, self.P[i + nDielectric])))
            Hy += complex(self.c2 * PHI[i] * self.dl * math.pi / 2 * 1j * 1 / math.sqrt(
                (M[0] - self.P[i + nDielectric][0]) ** 2 + (M[1] - self.P[i + nDielectric][1]) ** 2) *
                          (M[0] - self.P[i + nDielectric][0]) * (-self.hankelInfinity(self.k0, M, self.P[i + nDielectric])))
        Hx *= - complex(0, 1)
        Hy *= complex(0, 1)
        return [Ez, Hx, Hy]

    def __init__(self, k0, k1):
        self.k0 = k0
        self.k1 = k1
        self.c1 = (self.k1**2-self.k0**2)/(2*math.pi)
        self.c2 = 1 / (2 * math.pi)
        self.accuracy = 0.0000001
        self.ds = 0
        self.dl = 0
        self.P = []