from data.arc import Arc
from data.dielectricRectangle import DielectricRectangle
from data.source import Source
from visualization import Visualization

if __name__ == "__main__":
    #all angles in degrees
    #lower left point, width, height, rotateAngle
    dielectricRectangle = DielectricRectangle([0, 0], 1, 2, 0)
    #point
    source = Source([2, 2])
    #center, radius, angle, rotateAngle
    arc = Arc([-2, -2], 1, 30, -90)
    # task draw period, arc draw period, rectangle's points draw period, dielectric draw period
    visualization = Visualization(1, 1, 0.2, 0.1)
    visualization.drawTask(dielectricRectangle, source, arc)
    visualization.fillArc(arc, 10)
    visualization.fillDielectricRectangle(dielectricRectangle, 10, 10)
    visualization.blockPlot()