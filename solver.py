import math
import mpmath
import numpy as np

class Solver:

    def getInitialFieldStrength(self, k, P, P0):
        r = math.sqrt((P0[0] - P[0]) ** 2 + (P0[1] - P[1]) ** 2)
        r = r if r != 0 else self.accuracy
        return mpmath.hankel1(0, k * r)

    def G(self, k, M, P):
        r = math.sqrt((M[0] - P[0])**2 + (M[1] - P[1])**2)
        r = r if r != 0 else self.accuracy
        return math.pi/2 * 1j * mpmath.hankel1(0, k * r)

    def solve(self, nDielectric, nArc, dielectricRectangles, arcPoints, source):
        vertices = dielectricRectangles[0].getListOfVertices()
        self.ds = math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2) * \
             math.sqrt((vertices[1][0] - vertices[3][0])**2 + (vertices[1][1] - vertices[3][1])**2)
        self.dl = math.sqrt((arcPoints[0][0]-arcPoints[1][0])**2 + (arcPoints[0][1]-arcPoints[1][1])**2)
        B = []
        self.P = []
        for i in range(nDielectric):
            vertices = dielectricRectangles[i].getListOfVertices()
            self.P.append([vertices[1][0] - math.fabs(vertices[1][0] - vertices[2][0]) / 2,
                 vertices[1][1] - math.fabs(vertices[1][1] - vertices[2][1]) / 2])
            B.append(-complex(self.getInitialFieldStrength(self.k0, self.P[i], source.point)))
        for i in range(nArc):
            self.P.append([arcPoints[i][0], arcPoints[i][1]])
            B.append(-complex(self.getInitialFieldStrength(self.k0, self.P[i], source.point)))
        A = [[complex(0.0)] * (nDielectric+nArc) for i in range(nDielectric+nArc)]
        n = nDielectric+nArc
        for i in range(n):
            for j in range(n):
                i1 = 1 if i==j and j<nDielectric and i<nDielectric else 0
                if j<nDielectric:
                    A[i][j] = complex(self.c1*self.ds*(self.G(self.k0, self.P[i], self.P[j])-1/(self.c1*self.ds)*i1))
                else:
                    A[i][j] = complex(self.c2*self.dl*self.G(self.k0, self.P[i], self.P[j]))
        result = np.linalg.solve(np.array(A), np.array(B))
        U = result[:nDielectric]
        PHI = result[nDielectric:]
        return [U, PHI]

    def getFieldEInPointM(self, UPHI, M, source, nDielectric):
        U = UPHI[0]
        PHI = UPHI[1]
        Ez = complex(self.getInitialFieldStrength(self.k0, M, source.point))
        Hx = complex(1/math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2) *
                     (M[1] - source.point[1]) * (-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2))))
        Hy = complex(1/math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2) *
                     (M[0] - source.point[0]) * (-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - source.point[0]) ** 2 + (M[1] - source.point[1]) ** 2))))
        for i in range(len(U)):
            Ez += complex(self.c1*U[i]*self.G(self.k0, M, self.P[i])*self.ds)
            Hx += complex(self.c1*U[i]*self.ds*math.pi/2 * 1j*1/math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2)*
                          (M[1] - self.P[i][1])*(-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
            Hy += complex(self.c1*U[i]*self.ds*math.pi/2 * 1j*1/math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2)*
                          (M[0] - self.P[i][0])*(-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
        for i in range(len(PHI)):
            Ez += complex(self.c2*PHI[i]*self.G(self.k0, M, self.P[i+nDielectric])*self.dl)
            Hx += complex(self.c2*PHI[i]*self.dl*math.pi/2 * 1j*1/math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2)*
                          (M[1] - self.P[i][1])*(-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
            Hy += complex(self.c2*PHI[i]*self.dl*math.pi/2 * 1j*1/math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2)*
                          (M[0] - self.P[i][0])*(-mpmath.hankel1(1, self.k0*math.sqrt((M[0] - self.P[i][0]) ** 2 + (M[1] - self.P[i][1]) ** 2))))
        Hx *= - complex(0, 1)
        Hy *= complex(0, 1)
        return [Ez, Hx, Hy]

    def __init__(self, k0, k1):
        self.k0 = k0
        self.k1 = k1
        self.c1 = (self.k1**2-self.k0**2)/(2*math.pi)
        self.c2 = 1 / (2 * math.pi)
        self.accuracy = 0.000001
        self.ds = 0
        self.dl = 0
        self.P = []