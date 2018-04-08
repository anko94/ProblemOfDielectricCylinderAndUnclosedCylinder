from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from solver import Solver
from visualization import Visualization
import math
import matplotlib.pyplot as plt
import numpy as np


def drawTask(arcCenter, arcAngle, arcRadius, dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, sourcePoint):
    # all angles in degrees
    # lower left point, width, height, rotateAngle
    dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
    # point
    source = Source(sourcePoint)
    # center, radius, angle, rotateAngle
    arc = Arc(arcCenter, arcRadius, arcAngle*180/math.pi, -90)
    # task draw period, arc draw period, rectangle's points draw period, dielectric draw period
    visualization = Visualization(0.1, 0.1, 0.1, 0.1)
    visualization.drawTask(dielectricRectangle, source, arc)
    visualization.fillArc(arc, 40)
    visualization.fillDielectricRectangle(dielectricRectangle, 10, 10)
    visualization.blockPlot()


def plotFieldStrengthByAngle(arcAngle, PHI1, PHI2, PHI3):
    ax = plt.subplot(111)
    alpha1 = np.linspace(-arcAngle, arcAngle, len(PHI1))
    alpha2 = np.linspace(-arcAngle, arcAngle, len(PHI2))
    alpha3 = np.linspace(-arcAngle, arcAngle, len(PHI3))
    plt.plot(alpha1, PHI1, label="n=%d" % (len(PHI1),))
    plt.plot(alpha2, PHI2, label="n=%d" % (len(PHI2),))
    plt.plot(alpha3, PHI3, label="n=%d" % (len(PHI3),))

    leg = plt.legend(loc='best', ncol=1, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)

    plt.show()


def listAbs(list):
    absList = []
    for i in range(len(list)):
        absList.append(abs(list[i]))
    return absList


def norm(list, v):
    for i in range(len(list)):
        list[i] = list[i]/v
    return list


if __name__ == "__main__":
    arcCenter = [1, -1]
    arcAngle = 60 * math.pi/180          #angle in radians
    arcRadius = 1
    dielectricLowerLeftPoint = [0.5, -0.5]
    dielectricWidth = 0.4
    dielectricHeight = 1
    sourcePoint = [1, 1]

    nArcPoints = 10
    nDielectricWidthPoints = 7
    nDielectricHeightPoints = 7

    solver = Solver(2*math.pi,                     #k0  - волновое число вне диэлектрика
                    2*math.pi*1.000001,                     #k1  - волновое число внутри диэлектрика
                    1,                     #I   - амплитуда силы тока
                    8.854188*10**(-12),    #e0  - диэлектрическая проницаемость
                    4*math.pi*10**(-7))    #nu0 - магнитная проницаемость

    dielectricRectangle = DielectricRectangle([0, 0], 1, 2, -90)
    arc = Arc([1, -1], 1, 30, -90)
    source = Source([1, 1])
    result = solver.solve(nDielectricWidthPoints*nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints, nDielectricHeightPoints),
                          arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(nArcPoints)), source)
    PHI1 = result[1]

    nArcPoints = 20
    nDielectricWidthPoints = 7
    nDielectricHeightPoints = 7

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(nArcPoints)), source)
    PHI2 = result[1]

    nArcPoints = 40
    nDielectricWidthPoints = 7
    nDielectricHeightPoints = 7

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(nArcPoints)), source)
    PHI3 = result[1]

    absPHI1 = listAbs(PHI1)
    absPHI2 = listAbs(PHI2)
    absPHI3 = listAbs(PHI3)
    maxV = max([max(absPHI1), max(absPHI2), max(absPHI3)])

    plotFieldStrengthByAngle(arcAngle, norm(absPHI1, maxV), norm(absPHI2, maxV), norm(absPHI3, maxV))
    # drawTask(arcCenter, arcAngle, arcRadius, dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, sourcePoint)