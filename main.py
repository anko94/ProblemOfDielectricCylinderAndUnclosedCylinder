from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from solver import Solver
from visualization import Visualization
import math
import matplotlib.pyplot as plt
import numpy as np


def drawTask(arcCenter, arcAngle, arcRadius, dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, sourcePoint,
             nArcPoints, nDielectricWidthPoints, nDielectricHeightPoints):
    # all angles in degrees
    # lower left point, width, height, rotateAngle
    dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
    # point
    source = Source(sourcePoint)
    # center, radius, angle, rotateAngle
    arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    # task draw period, arc draw period, rectangle's points draw period, dielectric draw period
    visualization = Visualization(0.1, 0.1, 0.1, 0.1)
    visualization.drawTask(dielectricRectangle, source, arc)
    # visualization.fillArc(arc, nArcPoints)
    # visualization.fillDielectricRectangle(dielectricRectangle, nDielectricWidthPoints, nDielectricHeightPoints)
    visualization.blockPlot()


def plotCurrentByAngle(arcAngle, PHI1, PHI2, PHI3, PHI4, PHI5, PHI6, PHI7):
    arcAngle = arcAngle *math.pi/180
    ax = plt.subplot(111)
    ax.set_color_cycle(['orange', 'brown', 'yellow', 'blue', 'green', 'black', 'red'])
    PHIlist = [PHI1, PHI2, PHI3, PHI4, PHI5, PHI6, PHI7]
    for PHI in PHIlist:
        alpha = np.linspace(-arcAngle, arcAngle, len(PHI))
        plt.plot(alpha, PHI, label="n=%d" % (len(PHI),))
    plt.xlabel('угол экрана')
    plt.ylabel('плотность тока')
    leg = plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", ncol=3, mode="expand", shadow=True, fancybox=True, borderaxespad=0.)
    leg.get_frame().set_alpha(0.5)

    plt.show()


def plotFieldStrengthErrorByNumberOfPoints(nArcPointsList, maxU1, maxU2, maxU3, maxU4, maxU5, maxU6, maxU7, maxV):
    ax = plt.subplot(111)
    print(nArcPointsList)
    print([math.fabs(maxU1-maxU7)/maxV, math.fabs(maxU2-maxU7)/maxV, math.fabs(maxU3-maxU7)/maxV,
                              math.fabs(maxU4-maxU7)/maxV, math.fabs(maxU5-maxU7)/maxV, math.fabs(maxU6-maxU7)/maxV])
    plt.plot(nArcPointsList, [math.fabs(maxU1-maxU7)/maxV, math.fabs(maxU2-maxU7)/maxV, math.fabs(maxU3-maxU7)/maxV,
                              math.fabs(maxU4-maxU7)/maxV, math.fabs(maxU5-maxU7)/maxV, math.fabs(maxU6-maxU7)/maxV])
    plt.xlabel('число точек')
    plt.ylabel('погрешность')
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


def taskConvergence():
    arcCenter = [1, -1]
    arcAngle = 60  # angle in degrees
    arcRadius = 1
    dielectricLowerLeftPoint = [0.5, -0.5]
    dielectricWidth = 0.1
    dielectricHeight = 1
    sourcePoint = [1, 1]

    nArcPointsList = []

    nArcPoints = 10
    nDielectricWidthPoints = 10
    nDielectricHeightPoints = 10
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    solver = Solver(2 * math.pi,  # k0  - волновое число вне диэлектрика
                    2 * math.pi * 1.4,  # k1  - волновое число внутри диэлектрика
                    1,  # I   - амплитуда силы тока
                    8.854188 * 10 ** (-12),  # e0  - диэлектрическая проницаемость
                    4 * math.pi * 10 ** (-7))  # nu0 - магнитная проницаемость

    dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
    arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    source = Source(sourcePoint)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI1 = result[1]
    U1 = result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *= 2
    nDielectricHeightPoints = nDielectricHeightPoints
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI2 = result[1]
    U2= result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *= 2
    nDielectricHeightPoints = nDielectricHeightPoints
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI3 = result[1]
    U3 = result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *=2
    nDielectricHeightPoints =nDielectricHeightPoints
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI4 = result[1]
    U4 = result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *= 2
    nDielectricHeightPoints = nDielectricHeightPoints
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI5 = result[1]
    U5 = result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *= 2
    nDielectricHeightPoints = nDielectricHeightPoints
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI6 = result[1]
    U6 = result[0]

    nArcPoints *= 2
    nDielectricWidthPoints *= 2
    nDielectricHeightPoints = nDielectricHeightPoints

    result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                          dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                         nDielectricHeightPoints),
                          arc.breakUpArcByNPoints(nArcPoints), source)
    PHI7 = result[1]
    U7 = result[0]

    absPHI1 = listAbs(PHI1)
    absPHI2 = listAbs(PHI2)
    absPHI3 = listAbs(PHI3)
    absPHI4 = listAbs(PHI4)
    absPHI5 = listAbs(PHI5)
    absPHI6 = listAbs(PHI6)
    absPHI7 = listAbs(PHI7)
    absU1 = listAbs(U1)
    absU2 = listAbs(U2)
    absU3 = listAbs(U3)
    absU4 = listAbs(U4)
    absU5 = listAbs(U5)
    absU6 = listAbs(U6)
    absU7 = listAbs(U7)

    maxV = max([max(absPHI1), max(absPHI2), max(absPHI3), max(absPHI4), max(absPHI5), max(absPHI6), max(absPHI7)])

    plotCurrentByAngle(arcAngle, norm(absPHI1, maxV), norm(absPHI2, maxV), norm(absPHI3, maxV),
                             norm(absPHI4, maxV), norm(absPHI5, maxV),
                             norm(absPHI6, maxV), norm(absPHI7, maxV))

    maxV = max([max(absU1), max(absU2), max(absU3), max(absU4), max(absU5), max(absU6), max(absU7)])
    plotFieldStrengthErrorByNumberOfPoints(nArcPointsList, max(absU1), max(absU2), max(absU3), max(absU4), max(absU5), max(absU6), max(absU7), maxV)


if __name__ == "__main__":
    # arcCenter = [1, -1]
    # arcAngle = 60          #angle in degrees
    # arcRadius = 1
    # dielectricLowerLeftPoint = [0.5, -0.5]
    # dielectricWidth = 0.1
    # dielectricHeight = 1
    # sourcePoint = [1, 1]
    #
    # nArcPoints = 10
    # nDielectricWidthPoints = 10
    # nDielectricHeightPoints = 1
    #
    # solver = Solver(2*math.pi,                     #k0  - волновое число вне диэлектрика
    #                 2*math.pi*1.000001,                     #k1  - волновое число внутри диэлектрика
    #                 1,                     #I   - амплитуда силы тока
    #                 8.854188*10**(-12),    #e0  - диэлектрическая проницаемость
    #                 4*math.pi*10**(-7))    #nu0 - магнитная проницаемость
    #
    # dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
    # arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    # source = Source(sourcePoint)
    #
    # result = solver.solve(nDielectricWidthPoints*nDielectricHeightPoints, nArcPoints,
    #                       dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints, nDielectricHeightPoints),
    #                       arc.breakUpArcByNPoints(nArcPoints), source)
    # PHI1 = result[1]
    # drawTask(arcCenter, arcAngle, arcRadius, dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, sourcePoint,
    #          nArcPoints, nDielectricWidthPoints, nDielectricHeightPoints)
    taskConvergence()