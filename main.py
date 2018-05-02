from data.circle import Circle
from data.line import Line
from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from solver import Solver
from visualization import Visualization
import math
import matplotlib.pyplot as plt
import numpy as np


def drawTask(arcCenter, arcAngle, arcRadius, dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, sourcePoint,
             nArcPoints, nDielectricWidthPoints, nDielectricHeightPoints, figure, figureArray):
    two = 0 if len(dielectricLowerLeftPoint)==1 else 1
    # all angles in degrees
    # point
    source = Source(sourcePoint)
    # center, radius, angle, rotateAngle
    arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    if figure == "circle":
        # center, radius
        fig = Circle(figureArray[0], figureArray[1])
    else:
        #x, y
        fig = Line(figureArray[0], figureArray[1])
    # task draw period, arc draw period, rectangle's points draw period, dielectric draw period
    visualization = Visualization(0.1, 0.1, 0.1, 0.1)
    # lower left point, width, height, rotateAngle
    dielectricRectangle = [DielectricRectangle(dielectricLowerLeftPoint[0], dielectricWidth, dielectricHeight, -90)]
    if two == 1:
        dielectricRectangle.append(DielectricRectangle(dielectricLowerLeftPoint[1], dielectricWidth, dielectricHeight, -90))
    visualization.drawTask(dielectricRectangle, source, arc, figure, fig)
    # visualization.fillArc(arc, nArcPoints)
    # visualization.fillDielectricRectangle(dielectricRectangle, nDielectricWidthPoints, nDielectricHeightPoints)
    # if figure == "circle":
    #     visualization.fillCircle(fig, figureArray[2])
    # else:
    #     visualization.fillLine(fig, figureArray[2])
    visualization.blockPlot()


def plotCurrentByAngle(arcAngle, PHIlist):
    arcAngle = arcAngle *math.pi/180
    ax = plt.subplot(111)
    ax.set_color_cycle(['orange', 'brown', 'yellow', 'blue', 'green', 'black', 'red'])
    for PHI in PHIlist:
        alpha = np.linspace(-arcAngle, arcAngle, len(PHI))
        plt.plot(alpha, PHI, label="n=%d" % (len(PHI),))
    plt.xlabel('угол экрана')
    plt.ylabel('плотность тока')
    leg = plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", ncol=3, mode="expand", shadow=True, fancybox=True, borderaxespad=0.)
    leg.get_frame().set_alpha(0.5)

    plt.show()


def plotCurrentByAngle2(arcAngle, PHIlist, dws):
    arcAngle = arcAngle *math.pi/180
    ax = plt.subplot(111)
    ax.set_color_cycle(['orange', 'brown', 'yellow', 'blue', 'green', 'black', 'red','purple'])
    for i in range(len(PHIlist)):
        alpha = np.linspace(-arcAngle, arcAngle, len(PHIlist[i]))
        plt.plot(alpha, PHIlist[i], label="d=%.0e" % (dws[i],))
    plt.xlabel('угол экрана')
    plt.ylabel('плотность тока')
    leg = plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", ncol=3, mode="expand", shadow=True, fancybox=True, borderaxespad=0.)
    leg.get_frame().set_alpha(0.5)

    plt.show()


def plotFieldStrengthErrorByNumberOfPoints(nArcPointsList, maxU):
    ax = plt.subplot(111)
    print(nArcPointsList)
    maxV = max(maxU)
    maxU1 = []
    for i in range(len(maxU)-1):
        maxU1.append(math.fabs(maxU[i]-maxU[len(maxU)-1])/maxV)
    print(maxU1)
    plt.plot(nArcPointsList, maxU1)
    plt.xlabel('число точек')
    plt.ylabel('погрешность')
    plt.show()


def plotField(fieldE,maxE,figure,d):
    ax = plt.subplot(111)
    ax.set_color_cycle(['green', 'black', 'red', 'orange', 'brown', 'yellow', 'blue'])
    nameD = ["без диэлектрика", "парафин", "эбонит", "слюда", "стекло", "вода", "сегнетова соль" ]
    for i in range(len(fieldE)):
        plt.plot(d, norm(fieldE[i], maxE), label=nameD[i])
    if figure == "line":
        plt.xlabel('x')
    else:
        plt.xlabel('угол')
    plt.ylabel('поле Ez')
    leg = plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", ncol=3, mode="expand", shadow=True,
                     fancybox=True, borderaxespad=0.)
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
    nDielectricHeightPoints = 4
    nArcPointsList.append(nArcPoints + nDielectricWidthPoints * nDielectricHeightPoints)

    solver = Solver(2 * math.pi,  # k0  - волновое число вне диэлектрика
                    2 * math.pi * 1.4)  # k1  - волновое число внутри диэлектрика

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

    plotCurrentByAngle(arcAngle, [norm(absPHI1, maxV), norm(absPHI2, maxV), norm(absPHI3, maxV),
                             norm(absPHI4, maxV), norm(absPHI5, maxV),
                             norm(absPHI6, maxV), norm(absPHI7, maxV)])

    plotFieldStrengthErrorByNumberOfPoints(nArcPointsList, [max(absU1), max(absU2), max(absU3), max(absU4), max(absU5), max(absU6), max(absU7)])


def test2():
    arcCenter = [1, -1]
    arcAngle = 30  # angle in degrees
    arcRadius = 1
    dielectricLowerLeftPoint = [0.5, -0.5]
    dielectricWidth = 1
    dielectricHeight = 1
    sourcePoint = [1, 1]

    nArcPoints = 160
    nDielectricWidthPoints = 160
    nDielectricHeightPoints = 4

    solver = Solver(2 * math.pi,  # k0  - волновое число вне диэлектрика
                    2 * math.pi * 1.4)  # k1  - волновое число внутри диэлектрика

    arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    source = Source(sourcePoint)

    d = 1 / 10
    k = 1
    resultPHI = []
    resultU = []
    dws = []

    while k != 8:
        dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
        result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints, nArcPoints,
                              dielectricRectangle.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                             nDielectricHeightPoints),
                              arc.breakUpArcByNPoints(nArcPoints), source)
        absPHI = listAbs(result[1])
        absU = listAbs(result[0])
        resultPHI.append(absPHI)
        resultU.append(absU)
        dws.append(dielectricWidth)
        dielectricWidth *= d
        k += 1
    maxAbsPHI = []
    maxAbsU = []
    for i in range(len(resultPHI)):
        maxAbsPHI.append(max(resultPHI[i]))
        maxAbsU.append(max(resultU[i]))
    maxV = max(maxAbsPHI)
    maxV1 = max(maxAbsU)
    for i in range(len(resultPHI)):
        resultPHI[i] = norm(resultPHI[i], maxV)
        if i != len(resultPHI) - 1:
            maxAbsU[i] = math.fabs(maxAbsU[i] - maxAbsU[len(resultPHI) - 1]) / maxV1
    plotCurrentByAngle2(arcAngle, resultPHI, dws)
    print(maxAbsU)


def computeField(figure):
    arcCenter = [1, -1]
    arcAngle = 30  # angle in degrees
    arcRadius = 1
    dielectricLowerLeftPoint1 = [0.35, -1.666025]
    dielectricLowerLeftPoint2 = [1.35, -1.666025]
    dielectricWidth = 0.2
    dielectricHeight = 0.3
    sourcePoint = [1, 1]

    if figure == "line":
        # compute field in line
        eLineX = [2, 2]
        nx = 160
        eLineY = [-2.2, -1.4]
        line = Line(eLineX, eLineY)
        l = line.breakUpByNPoints(nx)
        x = l[0]
        y = l[1]
        figureArray = [eLineX, eLineY, nx]
        fieldComputeArray = [x, y, nx]
    else:
       # compute field in circle
       circleCenter = [1, -1]
       circleRadius = 512
       nCircle = 160
       circle = Circle(circleCenter, circleRadius)
       figureArray = [circleCenter, circleRadius, nCircle]
       fieldComputeArray = [circle.breakUpByNPoints(nCircle), nCircle]

    nArcPoints = 10
    nDielectricWidthPoints = 10
    nDielectricHeightPoints = 4

    arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    source = Source(sourcePoint)
    dielectricRectangle1 = DielectricRectangle(dielectricLowerLeftPoint1, dielectricWidth, dielectricHeight, -90)
    dielectricRectangle2 = DielectricRectangle(dielectricLowerLeftPoint2, dielectricWidth, dielectricHeight, -90)
    drawTask(arcCenter, arcAngle, arcRadius, [dielectricLowerLeftPoint1, dielectricLowerLeftPoint2], dielectricWidth, dielectricHeight, sourcePoint,
             nArcPoints, nDielectricWidthPoints, nDielectricHeightPoints, figure, figureArray)
    fieldE = []
    fieldEmax= []
    fieldHx = []
    fieldHy = []

    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1, dielectricRectangle2, source, arc, figure, fieldComputeArray, 1.000001)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 1.4)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 1.7)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 2.6)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 4)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 9)
    fieldE.append(result[0])
    fieldEmax.append(result[1])
    result = computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1,
                           dielectricRectangle2, source, arc, figure, fieldComputeArray, 22)
    fieldE.append(result[0])
    fieldEmax.append(result[1])

    maxE= max(fieldEmax)
    if figure == "line":
        graphArray=y
    else:
        angle = 0
        dAngle = 360/nCircle
        graphArray = []
        while math.fabs(angle - 360) >= 0.0000001:
            graphArray.append(angle)
            angle+=dAngle
    plotField(fieldE, maxE, figure, graphArray)


def computeField1(nDielectricWidthPoints, nDielectricHeightPoints, nArcPoints, dielectricRectangle1, dielectricRectangle2, source, arc, figure, fieldComputeArray, d):
    solver = Solver(2 * math.pi,  # k0  - волновое число вне диэлектрика
                    2 * math.pi * d)  # k1  - волновое число внутри диэлектрика
    fieldE = []
    fieldHx = []
    fieldHy = []
    n = fieldComputeArray[2] if figure=="line" else fieldComputeArray[1]
    for i in range(n):
        result = solver.solve(nDielectricWidthPoints * nDielectricHeightPoints * 2, nArcPoints,
                              dielectricRectangle1.breakUpRectangleByNMPoints(nDielectricWidthPoints,
                                                                              nDielectricHeightPoints) + dielectricRectangle2.breakUpRectangleByNMPoints(
                                  nDielectricWidthPoints,
                                  nDielectricHeightPoints),
                              arc.breakUpArcByNPoints(nArcPoints), source)
        if figure == "circle":
            M = fieldComputeArray[0][i]
        else:
            M = [fieldComputeArray[0], fieldComputeArray[1][i]]
        r = solver.getFieldEInPointM(result, M, source, nDielectricWidthPoints * nDielectricHeightPoints * 2)
        fieldE.append(r[0])
        fieldHx.append(r[1])
        fieldHy.append(r[2])

    fieldEAbs = listAbs(fieldE)
    # fieldHxAbs = listAbs(fieldHx)
    # fieldHyAbs = listAbs(fieldHy)

    maxE = max(fieldEAbs)
    # maxHx = max(fieldHxAbs)
    # maxHy = max(fieldHyAbs)
    return [fieldEAbs, maxE]


if __name__ == "__main__":
    # arcCenter = [1, -1]
    # arcAngle = 30  # angle in degrees
    # arcRadius = 1
    # dielectricLowerLeftPoint = [0.5, -0.5]
    # dielectricWidth = 0.3
    # dielectricHeight = 1
    # sourcePoint = [1, 1]
    #
    # eLineX = [0, 2]
    # nx = 40
    # eLineY = [-0.3, -0.3]
    # line = Line(eLineX, eLineY)
    # l = line.breakUpByNPoints(nx)
    # x = l[0]
    # y = l[1]
    #
    # nArcPoints = 20
    # nDielectricWidthPoints = 20
    # nDielectricHeightPoints = 4
    #
    # solver = Solver(2 * math.pi,  # k0  - волновое число вне диэлектрика
    #                 2 * math.pi * 1.000001)  # k1  - волновое число внутри диэлектрика
    #
    # arc = Arc(arcCenter, arcRadius, arcAngle, -90)
    # source = Source(sourcePoint)
    # dielectricRectangle = DielectricRectangle(dielectricLowerLeftPoint, dielectricWidth, dielectricHeight, -90)
    # test2()

    # circleCenter = [1, -1]
    # circleRadius = 3
    # nCircle = 10
    # figure="circle"
    # figureArray = [circleCenter, circleRadius, nCircle]

    # eLineX = [2, 2]
    # nx = 10
    # eLineY = [-2.2, -1.4]
    # figure = "line"
    # figureArray = [eLineX, eLineY, nx]

    # drawTask(arcCenter, arcAngle, arcRadius, [dielectricLowerLeftPoint], dielectricWidth, dielectricHeight, sourcePoint,
    #          nArcPoints, nDielectricWidthPoints, nDielectricHeightPoints, figure, figureArray)

    # taskConvergence()
    computeField("circle")