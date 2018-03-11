from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from solver import Solver
from visualization import Visualization


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
    print(len(U), len(PHI))
    print(U)
    print(PHI)
    # drawTask()