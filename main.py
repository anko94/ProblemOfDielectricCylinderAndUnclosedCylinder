from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from solver import Solver
from visualization import Visualization
import math


def drawTask():
    # all angles in degrees
    # lower left point, width, height, rotateAngle
    dielectricRectangle = DielectricRectangle([0, 0], 1, 2, -90)
    # point
    source = Source([2, 2])
    # center, radius, angle, rotateAngle
    arc = Arc([-2, -2], 1, 30, -90)
    # task draw period, arc draw period, rectangle's points draw period, dielectric draw period
    visualization = Visualization(0.1, 0.1, 0.1, 0.1)
    visualization.drawTask(dielectricRectangle, source, arc)
    visualization.fillArc(arc, 10)
    visualization.fillDielectricRectangle(dielectricRectangle, 10, 10)
    visualization.blockPlot()


if __name__ == "__main__":
    solver = Solver()
    dielectricRectangle = DielectricRectangle([0, 0], 1, 2, -90)
    arc = Arc([-2, -2], 1, 30, -90)
    result = solver.solve(100, 10, dielectricRectangle.breakUpRectangleByNMPoints(10, 10), arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(10)))
    U = result[0]
    PHI = result[1]
    result = solver.solve(200, 20, dielectricRectangle.breakUpRectangleByNMPoints(20, 10),
                          arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(20)))
    U1 = result[0]
    PHI1 = result[1]
    result = solver.solve(400, 40, dielectricRectangle.breakUpRectangleByNMPoints(40, 10),
                          arc.putVerticesInCorrectOrder(arc.breakUpArcByNPoints(40)))
    U2 = result[0]
    PHI2 = result[1]
    print(PHI[0], PHI1[0], PHI2[0])
    print(U[0], U1[0], U2[0])
    # drawTask()