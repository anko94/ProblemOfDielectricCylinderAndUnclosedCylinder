import math
import mpmath
import numpy as np


class Solver:

    def getInitialFieldStrength(self, e, nu, k, P, P0):
        r = math.sqrt((P0[0] - P[0]) ** 2 + (P0[1] - P[1]) ** 2)
        r = r if r != 0 else self.accuracy
        return -k*self.I*math.sqrt(nu)/(4*math.sqrt(e)) * mpmath.hankel1(0, k * r)

    def G(self, k, M, P):
        r = math.sqrt((M[0] - P[0])**2 + (M[1] - P[1])**2)
        r = r if r != 0 else self.accuracy
        return math.pi/2 * 1j * mpmath.hankel1(0, k * r)

    def solve(self, nDielectric, nArc, dielectricRectangles, arcPoints, source):
        vertices = dielectricRectangles[0].getListOfVertices()
        ds = math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2) * \
             math.sqrt((vertices[1][0] - vertices[3][0])**2 + (vertices[1][1] - vertices[3][1])**2)
        dl = math.sqrt((arcPoints[0][0]-arcPoints[1][0])**2 + (arcPoints[0][1]-arcPoints[1][1])**2)
        A = []
        B = []
        M = []
        for i in range(nDielectric):
            vertices = dielectricRectangles[i].getListOfVertices()
            M.append([vertices[1][0] - math.fabs(vertices[1][0] - vertices[2][0]) / 2,
                 vertices[1][1] - math.fabs(vertices[1][1] - vertices[2][1]) / 2])
            B.append(-complex(self.getInitialFieldStrength(self.e0, self.nu0, self.k0, M[i], source.point)))
        for i in range(nArc):
            M.append([arcPoints[i][0], arcPoints[i][1]])
            B.append(-complex(self.getInitialFieldStrength(self.e0, self.nu0, self.k0, M[i], source.point)))
        for i in range(nDielectric+nArc):
            A0Elem = []
            for j in range(nDielectric+nArc):
                i1 = 1 if i==j and j<nDielectric and i<nDielectric else 0
                if j<nDielectric:
                    A0Elem.append(complex(self.c1*ds*(self.G(self.k1, M[i], M[j])-1/(self.c1*ds)*i1)))
                else:
                    A0Elem.append(complex(self.c2*dl*self.G(self.k0, M[i], M[j])))
            A.append(A0Elem)
        result = np.linalg.solve(np.array(A), np.array(B))
        U = result[:nDielectric]
        PHI = result[nDielectric:]
        return [U, PHI]

    def __init__(self, k0, k1, I, e0, nu0):
        self.k0 = k0
        self.k1 = k1
        self.c1 = (self.k1**2-self.k0**2)/(2*math.pi)
        self.c2 = 1 / (2 * math.pi)
        self.accuracy = 0.000001
        self.I = I
        self.e0 = e0
        self.nu0 = nu0