import math
import mpmath
import numpy as np


class Solver:

    def G(self, k, M, P):
        r = math.sqrt((M[0] - P[0])**2 + (M[1] - P[1])**2) if \
            math.sqrt((M[0] - P[0])**2 + (M[1] - P[1])**2) != 0 else 0.000001
        return math.pi/2 * 1j * mpmath.hankel1(0, k * r)

    def solve(self, nDielectric, nArc, dielectricRectangles, arcPoints):
        k0=1
        k1=2
        c1=(k1**2-k0**2)/(2*math.pi)
        c2=1/(2*math.pi)
        U0S = [1.0j] * nDielectric
        U0L = [1.0j] * nArc
        vertices = dielectricRectangles[0].getListOfVertices()
        ds = math.sqrt((vertices[0][0] - vertices[1][0])**2 + (vertices[0][1] - vertices[1][1])**2) * \
             math.sqrt((vertices[1][0] - vertices[3][0])**2 + (vertices[1][1] - vertices[3][1])**2)
        dl = math.sqrt((arcPoints[0][0]-arcPoints[1][0])**2 + (arcPoints[0][1]-arcPoints[1][1])**2)
        A = []
        B = []
        for i in range(nDielectric):
            B.append(U0S[i])
        for i in range(nArc):
            B.append(U0L[i])
        for i in range(nDielectric+nArc):
            A0Elem = []
            if i<nDielectric:
                vertices = dielectricRectangles[i].getListOfVertices()
                M = [vertices[1][0]-math.sqrt(vertices[1][0]-vertices[2][0])/2,
                     vertices[1][1]-math.sqrt(vertices[1][1]-vertices[2][1])/2]
            else:
                M=[arcPoints[i-nDielectric][0], arcPoints[i-nDielectric][1]]
            for j in range(nDielectric+nArc):
                I = 1 if i==j and j<nDielectric and i<nDielectric else 0
                if j<nDielectric:
                    vertices = dielectricRectangles[j].getListOfVertices()
                    P = [vertices[1][0]-math.sqrt(vertices[1][0]-vertices[2][0])/2,
                         vertices[1][1]-math.sqrt(vertices[1][1]-vertices[2][1])/2]
                else:
                    P = [arcPoints[j-nDielectric][0], arcPoints[j-nDielectric][1]]
                A0Elem.append(complex(c1*ds*(self.G(k1, M, P)-1/(c1*ds)*I) + c2*dl*self.G(k0, M, P)))
            A.append(A0Elem)
        # print(len(A), len(A[0]), np.array(A))
        # print(len(B), np.array(B))
        result = np.linalg.solve(np.array(A), np.array(B))
        U = result[:nDielectric]
        PHI = result[nDielectric:]
        return [U, PHI]

    def __init__(self):
        pass